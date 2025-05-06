from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.database import get_text_collection
from app.model.text import TextInput, TextOutput
from bson import ObjectId
from fastapi import Depends, HTTPException
import logging
router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
@router.post("/changetoUpperCase", response_model=TextOutput)
async def changetouppercase(text:TextInput):
    logger.info(f"Received text for conversion: {text.text}")
    text_collection = await get_text_collection()
    reviewedtext = text.text.upper()
    storedtext = text.text
    logger.info(f"Converted text: {reviewedtext}")
    result = await text_collection.insert_one({"reviewedtext": reviewedtext, "storedtext": storedtext})
    return TextOutput(id=str(result.inserted_id), reviewedtext=reviewedtext, storedtext=storedtext)



@router.post("/changetoLowerCase", response_model=TextOutput)
async def changetolowercase(text:TextInput):
    logger.info(f"Received text for conversion: {text.text}")
    text_collection=await get_text_collection()
    reviewedtext=text.text.lower()
    logger.info(f"Converted text: {reviewedtext}")
    storedtext=text.text
    result=await text_collection.insert_one({"reviewedtext":reviewedtext,"storedtext":storedtext})
    return TextOutput(id=str(result.inserted_id), reviewedtext=reviewedtext, storedtext=storedtext)

@router.post("/reverseText", response_model=TextOutput)
async def reverseText(text:TextInput):
    logger.info(f"Received text for reversal: {text.text}")
    text_coolection=await get_text_collection()
    reviewedtext=text.text[::-1]
    logger.info(f"Reversed text: {reviewedtext}")
    storedtext=text.text
    result=await text_coolection.insert_one({"reviewedtext":reviewedtext,"storedtext":storedtext})
    return TextOutput(id=str(result.inserted_id), reviewedtext=reviewedtext, storedtext=storedtext)

@router.post("/countWordsandCharacters", response_model=TextOutput)
async def countWordsandCharacters(text:TextInput):
    logger.info(f"Received text for counting: {text.text}")
    text_collection=await get_text_collection()
    word_count=len(text.text.split())
    textwithoutspaces=text.text.replace(" ","")
    character_count=len(textwithoutspaces)
    reviewedtext=f"Word Count: {word_count}, Character Count: {character_count}"
    logger.info(f"Counted text: {reviewedtext}")
    storedtext=text.text
    result=await text_collection.insert_one({"reviewedtext":reviewedtext,"storedtext":storedtext})
    return TextOutput(id=str(result.inserted_id), reviewedtext=reviewedtext, storedtext=storedtext)

@router.post("convertanythingtohello", response_model=TextOutput)
async def convertanythingtohello(text:TextInput):
    logger.info(f"Received text for conversion to 'Hello': {text.text}")
    text_collection=await get_text_collection()
    reviewedtext="Hello"
    logger.info(f"Converted text: {reviewedtext}")
    storedtext=text.text
    result=await text_collection.insert_one({"reviewedtext":reviewedtext,"storedtext":storedtext})
    return TextOutput(id=str(result.inserted_id), reviewedtext=reviewedtext, storedtext=storedtext)
# @router.get("/getText/{item_id}", response_model=TextOutput)
# async def get_text(item_id: str, text_collection=Depends(get_text_collection)):
#     try:
#         object_id = ObjectId(item_id)
#         text_document = await text_collection.find_one({"_id": object_id})
#         if text_document:
#             return TextOutput(
#                 id=item_id,
#                 reviewedtext=text_document.get("reviewedtext"),
#                 storedtext=text_document.get("storedtext"),
#             )
#         else:
#             raise HTTPException(status_code=404, detail="Text not found")
#     except Exception:
#         raise HTTPException(status_code=400, detail="Invalid ID format")