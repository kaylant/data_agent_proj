"""CLI entry point for the agent"""

import time

from src.agent import build_graph, df
from src.data_loader import get_schema_summary


def main():
    print("=" * 50)
    print("Data Analysis Agent")
    print("=" * 50)
    print(f"Dataset: {len(df):,} rows × {len(df.columns)} columns")
    print("\nCommands:")
    print("  /schema - Show dataset schema")
    print("  /quit   - Exit & have a nice day.")
    print("=" * 50)

    app = build_graph()

    while True:
        try:
            question = input("\nYou: ").strip()

            if not question:
                continue
            if question == "/quit":
                print("Bye!")
                break
            if question == "/schema":
                print(get_schema_summary(df))
                continue

            start_time = time.time()
            result = app.invoke({"messages": [("user", question)]})
            elapsed = time.time() - start_time

            print(f"\nAgent: {result['messages'][-1].content}")
            print(f"\n[Response time: {elapsed:.2f}s]")

        except KeyboardInterrupt:
            print("\nBye!")
            break


if __name__ == "__main__":
    main()
