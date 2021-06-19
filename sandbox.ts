let data: string = await Deno.readTextFile('./README.md')

let tagMatch: RegExpExecArray | null;

const tagRe = /<img .*>/gm
const altRe = /alt\s*=\s*".*?"/g
const srcRe = /src\s*=\s*".*?"/g

do {
    tagMatch = tagRe.exec(data)
    if (!tagMatch)
        continue
    const tag: string = tagMatch[0]

    const altMatch = tag.match(altRe)
    if (!altMatch)
        continue
    const altWord = altMatch[0].split('"')[1]
    
    const srcMatch = tag.match(srcRe)
    if (!srcMatch)
        continue
    const srcWord = srcMatch[0].split('"')[1]

    const replace = `![${altWord}](${srcWord})`
    data = data.replace(tag, replace)
} while (tagMatch)

await Deno.writeTextFile('./README.md', data)