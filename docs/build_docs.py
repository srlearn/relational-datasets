# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

"""
# Build Docs

Build the documentation, which includes *pulling data from GitHub.*

## Usage

This requires that the `GH_TOKEN` is set with a valid GitHub OAuth token.
https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#authentication

```bash
cd docs/
export GH_TOKEN=your_token
python build_docs.py
```
"""

from datetime import datetime
import json
from os import environ
from urllib.request import Request
from urllib.request import urlopen

TOKEN = environ["GH_TOKEN"]
AUTHORIZATION = {"Authorization": f"token {TOKEN}"}

DATA_LOAD_RECOMMENDATION = """

=== "Python"

    ``` python
    from relational_datasets import load
    train, test = load("{dataset_name}", "{version}")
    ```

=== "Julia"

    ``` julia
    using RelationalDatasets
    train, test = load("{dataset_name}", "{version}")
    ```

"""


def build_dataset_descriptions(latest_version: str):

    req = Request(
        "https://api.github.com/repos/srlearn/datasets/releases/latest",
        headers=AUTHORIZATION,
    )

    with urlopen(req) as url:
        latest = json.loads(url.read().decode("utf-8"))

    for asset in latest["assets"]:
        name = asset["name"].split("_v")[0]

        req = Request(
            f"https://raw.githubusercontent.com/srlearn/datasets/main/srlearn/{name}/README.md",
            headers=AUTHORIZATION,
        )

        with urlopen(req) as url:
            description = url.read().decode("utf-8").splitlines()

        # Insert dataset loading instructions at the third position in the list.
        description.insert(
            2, DATA_LOAD_RECOMMENDATION.format(dataset_name=name, version=latest_version)
        )

        with open(f"dataset_descriptions/{name}.md", "w") as fh:
            for line in description:
                fh.write(line + "\n")


def build_downloads_page() -> str:

    req = Request(
        "https://api.github.com/repos/srlearn/datasets/git/refs/tags",
        headers=AUTHORIZATION,
    )

    with urlopen(req) as url:
        all_tags = json.loads(url.read().decode("utf-8"))

        # The response is formatted as {'ref': 'refs/tags/v0.0.1', ...}
        # so we taken the last item after splitting on '/' to get version numbers.
        all_versions = [tag["ref"].split("/")[-1] for tag in all_tags]
        all_versions.reverse()

    markdown_string = "# Download Datasets\n\n"
    markdown_string += (
        "Download links for each dataset and version are listed here:\n\n"
    )

    for version in all_versions:

        req = Request(
            f"https://api.github.com/repos/srlearn/datasets/releases/tags/{version}",
            headers=AUTHORIZATION,
        )

        with urlopen(req) as url:
            data = json.loads(url.read().decode("utf-8"))

        # I like timestamps
        stamp = datetime.fromisoformat(data["published_at"][:-1])

        markdown_string += (
            f"## Version {version} ({stamp.year}-{stamp.month}-{stamp.day})\n\n"
        )

        for asset in data["assets"]:

            name = asset["name"]

            _size = asset["size"]
            if _size > 1048576:
                size = round(_size / 1048576, 2)
                _unit = "MB"
            else:
                size = round(_size / 1024, 2)
                _unit = "KB"
            url = asset["browser_download_url"]

            markdown_string += f"- [{name}]({url}) ({size} {_unit})\n"

        markdown_string += "\n\n"

    with open("downloads.md", "w") as fh:
        fh.write(markdown_string)

    # The first entry of `all_versions` should be the most recent one.
    return all_versions[0]


if __name__ == "__main__":
    latest_version = build_downloads_page()
    build_dataset_descriptions(latest_version)
