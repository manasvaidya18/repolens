from app.config import settings
from indexing.repository_scanner import RepositoryScanner


def main():

    repository_id = "1206826196"

    local_path = (
        settings.storage_root
        / repository_id
    )

    repository_index = RepositoryScanner.scan(
        local_path
    )

    print("Repository indexed successfully.")
    print("Root path:", repository_index.root_path)
    print("Total files:", repository_index.total_files)
    print(
        "Total size:",
        repository_index.total_size_bytes,
        "bytes",
    )

    print("\nFirst 10 files:")

    for file in repository_index.files[:10]:
        print(
            f"- {file.relative_path} | "
            f"{file.extension or 'no extension'} | "
            f"{file.size_bytes} bytes"
        )


if __name__ == "__main__":
    main()