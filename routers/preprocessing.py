from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from .utils.audio import convert_audio, denoise_audio

router = APIRouter()


@router.post("/", summary="Предобработка аудиофайла.")
async def process_audio(file: Annotated[UploadFile, File(...)]):
    """Принимает на вход аудиофайл, конвертирует его в моноканальный
    WAV формат с частотой дескритизации 16 кГц.
    """
    try:
        input_format = file.filename.split(".")[-1].lower()

        converted_audio = convert_audio(file.file, input_format)
        denoised_audio = denoise_audio(converted_audio)

        return StreamingResponse(
            denoised_audio,
            media_type="audio/wav",
            headers={"Content-Disposition": f"attachment; filename=processed_{file.filename}.wav"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Preprocessing error: {str(e)}",
        )
