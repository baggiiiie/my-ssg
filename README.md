# my ssg

This is v2 of my ssg, still a bunch of stuff needed to be done, but i can't
deal with all these long procedural programming anymore.

## to do

Regarding what i should do for this project, the end goal is to make it
function as a standard SSG like [Quartz](https://quartz.jzhao.xyz/), or just
markdown presentation like Obsidian. So however they do it, i'll just treat it
as the standard. They also handles markdown in a very intuitive way, which
definitely brings more challenges to this project.

- i think the standard for quotes is, trailing double spaces will be converted
  to new lines, no trailing double spaces will join the current line with the
  next, just like in a paragraph. But Quartz and Obsidian don't really treat
  quotes like paragraphs which is more intuitive.

- currently no support for:

  - code block language support, no horizontal rule support.
  - no footnote support.
  - no multi-level list support.

- even more ambitious things:
  - preview of links like `![link-to-page]`
  - front matter

## next version

- get rid of all the procedural programming, make it more object-oriented i guess.
  - each line is an object, containing inline object, while consisting of block object
