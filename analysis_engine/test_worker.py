import asyncio

from services.worker import Worker


async def main():
    processed = await Worker.process_next_job()

    if processed:
        print("Job processed successfully.")
    else:
        print("No job processed.")


if __name__ == "__main__":
    asyncio.run(main())