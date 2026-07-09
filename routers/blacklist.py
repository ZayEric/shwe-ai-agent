from fastapi import APIRouter

from services.blacklist_service import search_blacklist

from services.openai_service import explain_result

router=APIRouter()

@router.post("/blacklist")

def blacklist(data:dict):

    result=search_blacklist(

        name=data.get("name"),

        nrc=data.get("nrc")

    )

    explanation=explain_result(result)

    return{

        "matched":len(result)>0,

        "records":result,

        "ai_summary":explanation

    }
