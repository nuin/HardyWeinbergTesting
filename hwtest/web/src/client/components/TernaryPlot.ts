import * as d3 from "d3";

interface ApiResponse {
  type: string;
  p_freq?: number;
  q_freq?: number;
  test_results: { test: string; p_value: number | null }[];
}

export class TernaryPlot {
  private readonly size = 400;
  private readonly margin = 50;

  render(container: HTMLElement, data: ApiResponse, nAlleles: number): void {
    // Ternary plot only meaningful for 2 alleles
    if (nAlleles !== 2 || data.type !== "two_allele") {
      container.textContent = "";
      return;
    }

    container.textContent = "";

    const width = this.size + 2 * this.margin;
    const height = this.size + 2 * this.margin;

    const svg = d3
      .select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    const g = svg.append("g").attr("transform", `translate(${this.margin}, ${this.margin})`);

    const S = this.size;

    // Triangle outline
    g.append("path")
      .attr("d", `M 0 ${S} L ${S / 2} 0 L ${S} ${S} Z`)
      .attr("fill", "none")
      .attr("stroke", "#333")
      .attr("stroke-width", 1);

    // HW equilibrium parabola: h = 2p(1-p)
    const parabolaPoints: [number, number][] = [];
    for (let i = 0; i <= 200; i++) {
      const p = i / 200;
      const h = 2 * p * (1 - p);
      const x = p * S;
      const y = S - h * S;
      parabolaPoints.push([x, y]);
    }

    const line = d3
      .line<[number, number]>()
      .x((d) => d[0])
      .y((d) => d[1]);

    g.append("path")
      .datum(parabolaPoints)
      .attr("d", line)
      .attr("fill", "none")
      .attr("stroke", "#333")
      .attr("stroke-width", 2);

    // Sample point
    if (data.p_freq !== undefined) {
      const pFreq = data.p_freq;
      const sampleX = pFreq * S;
      const hwH = 2 * pFreq * (1 - pFreq);
      const sampleY = S - hwH * S;

      g.append("circle")
        .attr("cx", sampleX)
        .attr("cy", sampleY)
        .attr("r", 6)
        .attr("fill", "#2563eb")
        .attr("stroke", "#1a1a2e")
        .attr("stroke-width", 1.5);
    }

    // Axis labels
    g.append("text")
      .attr("x", S / 2)
      .attr("y", S + 35)
      .attr("text-anchor", "middle")
      .attr("font-size", "12px")
      .text("p (allele frequency)");

    g.append("text")
      .attr("x", -35)
      .attr("y", S / 2)
      .attr("text-anchor", "middle")
      .attr("transform", `rotate(-90, -35, ${S / 2})`)
      .attr("font-size", "12px")
      .text("h (heterozygote freq.)");

    // Title
    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", 20)
      .attr("text-anchor", "middle")
      .attr("font-size", "14px")
      .attr("font-weight", "bold")
      .text("De Finetti Diagram");
  }
}
