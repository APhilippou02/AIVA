import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext,   WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import  openai, silero
from api import AssistantFunction
load_dotenv()

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "you are a voice assistant. your interface with users will be voice."
            "you should use short and concise responses, avoiding the usage of unpronounceable punctuation"
            "you should respond in tones resembling JARVIS from IRON MAN"
        )
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    function_ctx = AssistantFunction()

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        function_ctx=function_ctx,

    )
    assistant.start(ctx.room)
    await asyncio.sleep(1)
    await assistant.say("What can I help you with today ?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
