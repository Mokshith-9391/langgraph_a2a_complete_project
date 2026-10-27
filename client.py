import argparse
import asyncio
import httpx

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--supervisor", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    request = input("Enter task for supervisor: ").strip()
    if not request:
        return

    async with httpx.AsyncClient(timeout=180) as client:
        response = await client.post(
            f"{args.supervisor}/run",
            json={"request": request},
        )
        response.raise_for_status()
        data = response.json()

    print("\n===== RESEARCH =====\n")
    print(data["research"])
    print("\n===== FINAL ARTICLE =====\n")
    print(data["article"])

if __name__ == "__main__":
    asyncio.run(main())
