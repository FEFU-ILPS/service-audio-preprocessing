from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from .utils.audio import convert_audio, denoise_audio

router = APIRouter()


@router.post("/", summary="Предобработка аудиофайла.")
async def process_audio(file: Annotated[UploadFile, File(...)]) -> StreamingResponse:
    """Принимает на вход аудиофайл, конвертирует его в моноканальный
    WAV формат с частотой дескритизации 16 кГц.
    """
    file_bytes = await file.read()
    if len(file_bytes) % 4 != 0:  # 2 канала * 2 байта на выборку = 4 байта на фрейм
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect size of the PCM file. 16-bit PCM with 2 channels was expected.",
        )

    try:
        converted_audio = convert_audio(file_bytes)
        denoised_audio = denoise_audio(converted_audio)

        return StreamingResponse(
            denoised_audio,
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=preprocessed_audio.wav",
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Preprocessing error: {str(e)}",
        )
