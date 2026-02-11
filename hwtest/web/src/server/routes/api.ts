import { Router, type Request, type Response } from "express";

const router = Router();

const FASTAPI_URL = process.env.FASTAPI_URL || "http://localhost:8000";

/**
 * POST /api/test
 * Proxies the request to the Python FastAPI backend.
 */
router.post("/test", async (req: Request, res: Response) => {
  try {
    const response = await fetch(`${FASTAPI_URL}/api/test`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    if (!response.ok) {
      const error = await response.json();
      res.status(response.status).json(error);
      return;
    }

    const data = await response.json();
    res.json(data);
  } catch (err) {
    res.status(502).json({
      error: "Failed to connect to the Python backend. Is the FastAPI server running?",
    });
  }
});

/**
 * GET /api/health
 * Checks connectivity to the FastAPI backend.
 */
router.get("/health", async (_req: Request, res: Response) => {
  try {
    const response = await fetch(`${FASTAPI_URL}/health`);
    const data = await response.json();
    res.json({ proxy: "ok", backend: data });
  } catch {
    res.json({ proxy: "ok", backend: "unreachable" });
  }
});

export { router as apiRouter };
