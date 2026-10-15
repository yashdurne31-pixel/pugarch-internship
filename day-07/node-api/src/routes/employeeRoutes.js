import { Router } from "express";
import { employeeController as c } from "../controllers/employeeController.js";
const router = Router();
router.get("/", c.list);
router.get("/:id", c.get);
router.post("/", c.create);
router.put("/:id", c.update);
router.delete("/:id", c.remove);
export default router;
