import * as d3 from "d3";

interface ApiResponse {
  type: string;
  n?: number;
  d?: number;
  h?: number;
  r?: number;
  p_freq?: number;
  q_freq?: number;
  test_results: { test: string; p_value: number | null }[];
}

/**
 * De Finetti diagram matching the style from Santos, Lemes & Otto (2020).
 *
 * The plot is a triangle where:
 *   - Bottom-left corner = all aa (p=0, h=0)
 *   - Bottom-right corner = all AA (p=1, h=0)
 *   - Top vertex = all Aa (h=1)
 * x-axis: allele frequency p = (D + H/2) / N
 * y-axis: heterozygote frequency h = H / N
 * HW parabola: h = 2p(1-p)
 * 95% confidence bands: h = 2p(1-p)(1 ± sqrt(chi2_crit / N))
 */
export class TernaryPlot {
  render(container: HTMLElement, data: ApiResponse, nAlleles: number): void {
    container.textContent = "";

    if (nAlleles !== 2 || data.type !== "two_allele" || data.p_freq === undefined) {
      return;
    }

    const margin = { top: 40, right: 30, bottom: 50, left: 55 };
    const width = 460;
    const height = 460;
    const plotW = width - margin.left - margin.right;
    const plotH = height - margin.top - margin.bottom;
    const pFreq = data.p_freq;
    const critChi2 = 3.8415; // alpha=0.05, df=1

    const svg = d3.select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", `0 0 ${width} ${height}`);

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Scales
    const xScale = d3.scaleLinear().domain([0, 1]).range([0, plotW]);
    const yScale = d3.scaleLinear().domain([0, 1]).range([plotH, 0]);

    // Triangle boundary (feasible region)
    const trianglePath = [
      [xScale(0), yScale(0)],
      [xScale(0.5), yScale(1)],
      [xScale(1), yScale(0)],
    ] as [number, number][];

    g.append("path")
      .attr("d", d3.line()(trianglePath) + "Z")
      .attr("fill", "#fafafa")
      .attr("stroke", "#333")
      .attr("stroke-width", 1.2);

    // Axes
    // x-axis (bottom)
    const xAxis = d3.axisBottom(xScale).ticks(10).tickSize(4);
    g.append("g")
      .attr("transform", `translate(0,${plotH})`)
      .call(xAxis)
      .selectAll("text").attr("font-size", "10px");

    // y-axis (left)
    const yAxis = d3.axisLeft(yScale).ticks(10).tickSize(4);
    g.append("g")
      .call(yAxis)
      .selectAll("text").attr("font-size", "10px");

    // Axis labels
    g.append("text")
      .attr("x", plotW / 2)
      .attr("y", plotH + 38)
      .attr("text-anchor", "middle")
      .attr("font-size", "12px")
      .attr("font-style", "italic")
      .text("p");

    g.append("text")
      .attr("x", -plotH / 2)
      .attr("y", -40)
      .attr("text-anchor", "middle")
      .attr("transform", "rotate(-90)")
      .attr("font-size", "12px")
      .attr("font-style", "italic")
      .text("h");

    // Corner labels
    g.append("text")
      .attr("x", xScale(0))
      .attr("y", yScale(0) + 14)
      .attr("text-anchor", "middle")
      .attr("font-size", "9px")
      .attr("fill", "#666")
      .text("q = 1");

    g.append("text")
      .attr("x", xScale(1))
      .attr("y", yScale(0) + 14)
      .attr("text-anchor", "middle")
      .attr("font-size", "9px")
      .attr("fill", "#666")
      .text("p = 1");

    // HW equilibrium parabola: h = 2p(1-p)
    const nPoints = 300;
    const parabolaData: [number, number][] = [];
    for (let i = 0; i <= nPoints; i++) {
      const p = i / nPoints;
      const h = 2 * p * (1 - p);
      parabolaData.push([xScale(p), yScale(h)]);
    }

    g.append("path")
      .datum(parabolaData)
      .attr("d", d3.line<[number, number]>().x(d => d[0]).y(d => d[1]))
      .attr("fill", "none")
      .attr("stroke", "#333")
      .attr("stroke-width", 1.8);

    // 95% confidence bands
    // We need N to compute bands; estimate from p_freq and the fact
    // the API doesn't return N directly. Use chi2_crit/N relationship.
    // For now, draw bands assuming N=200 (standard example).
    // A better approach would be to return N from the API.
    const N = this.estimateN(data);
    if (N > critChi2) {
      const fVal = Math.sqrt(critChi2 / N);

      // Lower band: h = 2p(1-p)(1 - sqrt(chi2/N))
      const lowerData: [number, number][] = [];
      for (let i = 0; i <= nPoints; i++) {
        const p = i / nPoints;
        const h = 2 * p * (1 - p) * (1 - fVal);
        if (h >= 0) {
          lowerData.push([xScale(p), yScale(h)]);
        }
      }

      // Upper band: h = 2p(1-p)(1 + sqrt(chi2/N))
      const upperData: [number, number][] = [];
      for (let i = 0; i <= nPoints; i++) {
        const p = i / nPoints;
        const fNeg = -fVal;
        const h = 2 * p * (1 - p) * (1 + fVal);
        // Clip to triangle: h <= min(2p, 2(1-p)) = 2*min(p, 1-p)
        if (h <= 2 * Math.min(p, 1 - p) &&
            fNeg * (1 - p) >= -p && fNeg * p >= p - 1) {
          upperData.push([xScale(p), yScale(h)]);
        }
      }

      const bandLine = d3.line<[number, number]>().x(d => d[0]).y(d => d[1]);

      g.append("path")
        .datum(lowerData)
        .attr("d", bandLine)
        .attr("fill", "none")
        .attr("stroke", "#888")
        .attr("stroke-width", 1)
        .attr("stroke-dasharray", "4,3");

      g.append("path")
        .datum(upperData)
        .attr("d", bandLine)
        .attr("fill", "none")
        .attr("stroke", "#888")
        .attr("stroke-width", 1)
        .attr("stroke-dasharray", "4,3");
    }

    // Vertical dashed line at observed p
    g.append("line")
      .attr("x1", xScale(pFreq))
      .attr("x2", xScale(pFreq))
      .attr("y1", yScale(0))
      .attr("y2", yScale(2 * pFreq * (1 - pFreq)))
      .attr("stroke", "#2563eb")
      .attr("stroke-width", 0.8)
      .attr("stroke-dasharray", "2,2")
      .attr("opacity", 0.4);

    // Observed sample point: x = (D + H/2)/N, y = H/N
    if (data.d !== undefined && data.h !== undefined && data.n !== undefined && data.n > 0) {
      const obsX = (data.d + data.h / 2) / data.n;
      const obsY = data.h / data.n;

      g.append("circle")
        .attr("cx", xScale(obsX))
        .attr("cy", yScale(obsY))
        .attr("r", 5)
        .attr("fill", "#dc2626")
        .attr("stroke", "#7f1d1d")
        .attr("stroke-width", 1.5);

      g.append("text")
        .attr("x", xScale(obsX) + 8)
        .attr("y", yScale(obsY) + 4)
        .attr("font-size", "9px")
        .attr("fill", "#dc2626")
        .text("observed");
    }

    // Expected point on parabola (HW equilibrium)
    const hwH = 2 * pFreq * (1 - pFreq);
    g.append("circle")
      .attr("cx", xScale(pFreq))
      .attr("cy", yScale(hwH))
      .attr("r", 5)
      .attr("fill", "#2563eb")
      .attr("stroke", "#1a1a2e")
      .attr("stroke-width", 1.5);

    g.append("text")
      .attr("x", xScale(pFreq) + 8)
      .attr("y", yScale(hwH) - 8)
      .attr("font-size", "9px")
      .attr("fill", "#2563eb")
      .text("expected");

    // Small inset triangle (d, h, r relationship) in top-right
    this.drawInsetTriangle(g, plotW);

    // Title
    svg.append("text")
      .attr("x", width / 2)
      .attr("y", 22)
      .attr("text-anchor", "middle")
      .attr("font-size", "13px")
      .attr("font-weight", "bold")
      .text("De Finetti Diagram");

    // Band label
    if (N > critChi2) {
      g.append("text")
        .attr("x", plotW - 5)
        .attr("y", plotH - 8)
        .attr("text-anchor", "end")
        .attr("font-size", "8px")
        .attr("fill", "#888")
        .text("95% CI bands (dashed)");
    }
  }

  /**
   * Draw the small inset triangle showing the d-h-r coordinate system,
   * matching the original publication's figure.
   */
  private drawInsetTriangle(g: d3.Selection<SVGGElement, unknown, null, undefined>, plotW: number): void {
    const cx = plotW - 55;
    const cy = 30;
    const s = 35;

    // Small triangle
    const pts: [number, number][] = [
      [cx, cy - s * 0.6],       // top (h)
      [cx - s * 0.6, cy + s * 0.4], // bottom-left (p)
      [cx + s * 0.6, cy + s * 0.4], // bottom-right (q)
    ];

    g.append("path")
      .attr("d", d3.line()(pts) + "Z")
      .attr("fill", "none")
      .attr("stroke", "#666")
      .attr("stroke-width", 0.8);

    // Dot in center
    g.append("circle")
      .attr("cx", cx)
      .attr("cy", cy)
      .attr("r", 2)
      .attr("fill", "#666");

    // Dashed line from dot to base
    g.append("line")
      .attr("x1", cx)
      .attr("x2", cx)
      .attr("y1", cy)
      .attr("y2", cy + s * 0.4)
      .attr("stroke", "#666")
      .attr("stroke-width", 0.6)
      .attr("stroke-dasharray", "2,1");

    // Dashed lines to sides
    g.append("line")
      .attr("x1", cx)
      .attr("x2", cx - s * 0.35)
      .attr("y1", cy)
      .attr("y2", cy - s * 0.1)
      .attr("stroke", "#666")
      .attr("stroke-width", 0.6)
      .attr("stroke-dasharray", "2,1");

    g.append("line")
      .attr("x1", cx)
      .attr("x2", cx + s * 0.35)
      .attr("y1", cy)
      .attr("y2", cy - s * 0.1)
      .attr("stroke", "#666")
      .attr("stroke-width", 0.6)
      .attr("stroke-dasharray", "2,1");

    // Labels
    g.append("text").attr("x", cx).attr("y", cy + s * 0.65).attr("text-anchor", "middle").attr("font-size", "8px").attr("fill", "#666").text("h");
    g.append("text").attr("x", cx - s * 0.5).attr("y", cy - s * 0.15).attr("text-anchor", "middle").attr("font-size", "8px").attr("fill", "#666").text("d");
    g.append("text").attr("x", cx + s * 0.5).attr("y", cy - s * 0.15).attr("text-anchor", "middle").attr("font-size", "8px").attr("fill", "#666").text("r");
    g.append("text").attr("x", cx - s * 0.7).attr("y", cy + s * 0.55).attr("text-anchor", "middle").attr("font-size", "8px").attr("fill", "#666").text("p");
    g.append("text").attr("x", cx + s * 0.7).attr("y", cy + s * 0.55).attr("text-anchor", "middle").attr("font-size", "8px").attr("fill", "#666").text("q");
  }

  private estimateN(data: ApiResponse): number {
    return data.n ?? 200;
  }
}
