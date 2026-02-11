import express from "express";
import { apiRouter } from "./routes/api.js";

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use("/api", apiRouter);

// Serve static files in production
app.use(express.static("dist/client"));

app.listen(PORT, () => {
  console.log(`HW_TEST web server running on http://localhost:${PORT}`);
});
