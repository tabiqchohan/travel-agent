from fastapi import APIRouter

from ..schemas.budget import BudgetEstimateRequest, BudgetEstimateResponse
from ..services.budget_service import BudgetService

router = APIRouter(prefix="/budget", tags=["Budget"])


@router.post("/estimate", response_model=BudgetEstimateResponse)
async def estimate_budget(req: BudgetEstimateRequest):
    service = BudgetService()
    return await service.estimate(req)
