#!python3

# MIT License
#
# Copyright © 2021 John Scott.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
from xml.etree import ElementTree
import os

def main():
    parser = argparse.ArgumentParser(description='Visualise a collection of storyboards as a unified directed graph')
    parser.add_argument('storyboard', nargs='+', help='Path to Storyboards')
    args = parser.parse_args()

    print(f"graph TD")

    builder = TreeBuilder()

    for storyboard_path in args.storyboard:
        storyboard_name = os.path.splitext(os.path.basename(storyboard_path))[0]

        builder.currentStoryboardName = storyboard_name
        ElementTree.parse(storyboard_path, ElementTree.XMLParser(target=builder))

    builder.finalize()

class TreeBuilder(ElementTree.TreeBuilder):

    def __init__(self):
        self.lastComment = None
        self.currentStoryboardName = None
        self.mainSceneObjectId = None
        self.links = set()
        self.stack = list()
        self.previousTag = None

    def finalize(self):
        print()
        for link in self.links:
            print(link)

    def comment(self, data):
        # print(data)
        self.lastComment = data

    def start(self, tag, attrs):

        if tag == 'document':
            print(f"  subgraph {self.currentStoryboardName}")

        if 'initialViewController' in attrs:
            print(f"    {self.currentStoryboardName}_([ ])")
            self.links.add(f"{self.currentStoryboardName}_ --> {attrs['initialViewController']}")

        if 'storyboardIdentifier' in attrs:
            print(f"    {self.currentStoryboardName}_{attrs['storyboardIdentifier']}([{attrs['storyboardIdentifier']}])")
            self.links.add(f"{self.currentStoryboardName}_{attrs['storyboardIdentifier']} -.-> {attrs['id']}")

        if self.previousTag == 'objects' and 'id' in attrs:
            self.mainSceneObjectId = attrs['id']
            print(f"    {self.mainSceneObjectId}[{self.lastComment}]")

        if tag == 'viewControllerPlaceholder':
            self.links.add(f"{self.mainSceneObjectId} -.-> {attrs['storyboardName']}_{attrs.get('referencedIdentifier','')}")

        if tag == 'segue':
            if self.mainSceneObjectId is None and 'scene' in self.stack:
                raise ValueError(f"Missing mainSceneObjectId in {self.currentStoryboardName} {attrs}")
            if 'destination' in attrs:
                self.links.add(f"{self.mainSceneObjectId} -->|{attrs.get('identifier',' ')}| {attrs['destination']}")
            # else:
            #     exit(f"{attrs}")

        if 'exit' == tag:
            if self.mainSceneObjectId is None and 'scene' in self.stack:
                raise ValueError(f"Missing mainSceneObjectId in {self.currentStoryboardName} {attrs}")
            print(f"    {attrs['id']}[[{attrs['userLabel']}]]")
            self.links.add(f"{self.mainSceneObjectId} --> {attrs['id']}")
        self.stack.append(tag)

        self.previousTag = tag


    def end(self, tag):
        self.stack.pop()
        if tag == 'document':
            self.currentStoryboardName = None
            print(f"  end")
        elif tag == 'scene':
            self.mainSceneObjectId = None


def parse_node(node, *stack):

    print("  " * len(stack), node.tag)

    for subnode in node:
        parse_node(subnode, node.tag, *stack)


def compile_pattern(pattern):
    pattern = re.sub(r'{(\d+)}', '{{\\1}}', pattern)
    try:
        return re.compile(pattern, flags=re.MULTILINE|re.DOTALL)
    except Exception as e:
        print(pattern)
        raise

if __name__ == "__main__":
    main()
