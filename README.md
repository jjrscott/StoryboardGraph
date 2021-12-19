# StoryboardGraph

This experimental script takes a collection of [Storyboard](https://developer.apple.com/library/archive/documentation/ToolsLanguages/Conceptual/Xcode_Overview/DesigningwithStoryboards.html) files and produces a unified chart in [Mermaid](https://mermaid-js.github.io).

For example it can takes storyboards that look like this:

<img src="images/interface-builder.png" width="485">

and produces a chart like this:

<img src="images/mermaid.svg" width="300">

## Usage

```shell
usage: storyboard-graph.py [-h] storyboard [storyboard ...]

Visualise a collection of storyboards as a unified directed graph

positional arguments:
  storyboard  Path to Storyboards

optional arguments:
  -h, --help  show this help message and exit
```

## Example

```shell
python3 storyboard-graph.py examples/*.storyboard
```

```mermaid
graph TD
  subgraph LaunchScreen
    LaunchScreen_([ ])
    01J-lp-oVM[View Controller]
  end
  subgraph Main
    Main_([ ])
    opT-ub-mb2[Root View Controller]
    cHQ-dZ-cMg[Collection View Controller]
    TfI-UL-sU5[Navigation Controller]
  end

TfI-UL-sU5 -->| | opT-ub-mb2
Main_ --> TfI-UL-sU5
opT-ub-mb2 -->| | cHQ-dZ-cMg
LaunchScreen_ --> 01J-lp-oVM
```
