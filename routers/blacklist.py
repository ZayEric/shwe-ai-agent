from fastapi import APIRouter
import traceback

from services.blacklist_service import search_blacklist
from services.openai_service import explain_result

router = APIRouter()


@router.post("/blacklist")
def blacklist(data: dict):
   
    try:

        print("========== VERSION 17 JULY ==========")
        print("Incoming JSON:", data)

        name = data.get("Name") or data.get("name")
        nrc = data.get("NRC") or data.get("nrc")

        print("Name:", repr(name))
        print("NRC:", repr(nrc))

        result = search_blacklist(name=name, nrc=nrc)

        print("Search Result:", result)

        if result:
            explanation = explain_result(result)
        else:
            explanation = "No blacklist match found."

        return {
            "matched": len(result) > 0,
            "records": result,
            "ai_summary": explanation
        }

    except Exception as e:
        traceback.print_exc()

        return {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
