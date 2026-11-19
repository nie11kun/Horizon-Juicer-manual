"use strict";
const path = require("path");
const fs = require("fs");
const { spawn } = require("child_process");

const parse = require("honkit/lib/parse").default;
const outputMod = require("honkit/lib/output").default;
const getBook = require("honkit/lib/cli/getBook").default;
const website = require("honkit/lib/output/website").default;
const jsonMod = require("honkit/lib/json").default;
const templating = require("honkit/lib/templating").default;
const writeFile = require("honkit/lib/output/helper/writeFile").default;
const getConvertOptions = require("honkit/lib/output/ebook/getConvertOptions").default;
const promise = require("honkit/lib/utils/promise").default;

const inputDir = path.resolve(process.argv[2] || ".");
const outputFile = path.resolve(process.argv[3] || "./output.pdf");
const outputFolder = path.resolve(inputDir, "_ebook_tmp");

const defaultCalibreExe = "C:\\Program Files\\Calibre2\\ebook-convert.exe";
const ebookConvertBin = fs.existsSync(defaultCalibreExe) ? defaultCalibreExe : "ebook-convert";

function cleanupTmp() {
    if (fs.existsSync(outputFolder)) {
        fs.rmSync(outputFolder, { recursive: true, force: true });
    }
}

cleanupTmp();
fs.mkdirSync(outputFolder, { recursive: true });

const book = getBook([inputDir], { log: "info" });
const logger = book.getLogger();
const baseGenerator = outputMod.getGenerator("ebook");

const CustomEbookGenerator = Object.assign({}, baseGenerator, {
    onFinish(out) {
        const options = out.getOptions();
        const prefix = options.get("prefix");
        const summaryName = "SUMMARY.html";
        const engine = website.createTemplateEngine(out, summaryName);
        const context = jsonMod.encodeOutput(out);

        return templating
            .renderFile(engine, `${prefix}/summary.html`, context)
            .then((tplOut) => writeFile(out, summaryName, tplOut.getContent()))
            .then(() => getConvertOptions(out))
            .then((convertOpts) => {
                const summaryHtml = path.resolve(outputFolder, summaryName);
                const argv = [summaryHtml, outputFile];
                for (const [key, val] of Object.entries(convertOpts)) {
                    if (val === null || val === undefined || val === false) {
                        continue;
                    }
                    if (typeof val === "boolean") {
                        argv.push(key);
                    } else {
                        argv.push(`${key}=${String(val)}`);
                    }
                }
                logger.info.ln(`running ebook-convert -> ${outputFile}`);
                const d = promise.defer();
                const child = spawn(ebookConvertBin, argv, {
                    stdio: "inherit",
                    windowsHide: true
                });
                child.on("error", (err) => d.reject(err));
                child.on("close", (code) => {
                    if (code === 0) {
                        d.resolve(out);
                    } else {
                        d.reject(new Error(`ebook-convert exited with code ${code}`));
                    }
                });
                return d.promise;
            });
    }
});

Promise.resolve(
    parse.parseBook(book).then((resultBook) =>
        outputMod.generate(CustomEbookGenerator, resultBook, {
            root: outputFolder,
            format: "pdf"
        })
    )
)
    .then(() => {
        logger.info.ok(`PDF generated successfully: ${outputFile}`);
        cleanupTmp();
    })
    .catch((err) => {
        cleanupTmp();
        console.error(err);
        process.exit(1);
    });
