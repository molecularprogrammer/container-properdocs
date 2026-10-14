import base64
import logging
import os
import re
import subprocess
from html import escape

from markdown.preprocessors import Preprocessor
from markdown.util import AtomicString


logger = logging.getLogger(__name__)

PLANTUML_JAR = os.environ.get(
    "PLANTUML_JAR",
    "/opt/plantuml/plantuml.jar",
)


class DitaaFencePreprocessor(Preprocessor):
    """
    Convert:

        ```ditaa{kroki=true}

    to:

        ```ditaa

    before SuperFences processes the document.

    Markdown Preview Enhanced still sees the original source.
    """

    FENCE_RE = re.compile(
        r"^(?P<indent>[ ]*)"
        r"(?P<fence>`{3,}|~{3,})"
        r"ditaa"
        r"\{kroki\s*=\s*true\}"
        r"[ \t]*$",
        re.IGNORECASE,
    )

    def run(self, lines):
        result = []

        for line in lines:
            match = self.FENCE_RE.match(line)

            if match:
                result.append(
                    f"{match.group('indent')}"
                    f"{match.group('fence')}"
                    f"ditaa"
                )
            else:
                result.append(line)

        return result


def ditaa_fence(
    source,
    language,
    css_class,
    options,
    md,
    **kwargs,
):
    """
    Render a Ditaa fenced block using the local PlantUML JAR.

    PlantUML produces PNG, which is embedded as a base64 data URI.
    """

    source = source.strip()

    # plantuml_markdown may have wrapped the source in
    # @startuml / @enduml. Remove those wrappers if present.
    if source.startswith("@startuml"):
        source = source[len("@startuml"):].lstrip()

    if source.endswith("@enduml"):
        source = source[:-len("@enduml")].rstrip()

    plantuml_source = (
        "@startditaa\n"
        + source
        + "\n@endditaa\n"
    )

    logger.debug("========== DITAA FENCE CALLED ==========")
    logger.debug("Ditaa source:\n%s", plantuml_source)

    cmd = [
        "java",
        "-Djava.awt.headless=true",
        "-jar",
        PLANTUML_JAR,
        "-p",
        "-tpng",
        "-charset",
        "UTF-8",
    ]

    try:
        result = subprocess.run(
            cmd,
            input=plantuml_source.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        logger.exception("Unable to execute PlantUML")
        return (
            '<div class="ditaa-error">'
            f"Unable to execute PlantUML: {escape(str(exc))}"
            "</div>"
        )

    stderr = result.stderr.decode("utf-8", errors="replace")

    logger.debug("PlantUML return code: %s", result.returncode)
    logger.debug("PlantUML stderr:\n%s", stderr)
    logger.debug("PlantUML stdout length: %d", len(result.stdout))

    if result.returncode != 0:
        return (
            '<div class="ditaa-error">'
            "<strong>PlantUML failed</strong><pre>"
            f"{escape(stderr)}"
            "</pre></div>"
        )

    png = result.stdout

    if not png:
        return (
            '<div class="ditaa-error">'
            "PlantUML returned no image data."
            "</div>"
        )

    # Verify that PlantUML actually returned a PNG.
    if not png.startswith(b"\x89PNG"):
        logger.error(
            "PlantUML returned unexpected data: %r",
            png[:32],
        )
        return (
            '<div class="ditaa-error">'
            "PlantUML returned unexpected image data."
            "</div>"
        )

    encoded = base64.b64encode(png).decode("ascii")

    img = (
        '<img'
        ' class="ditaa"'
        ' src="data:image/png;base64,'
        + encoded
        + '"'
        ' alt="DITAA diagram"'
        '>'
    )

    return md.htmlStash.store(
        AtomicString(img)
    )


def makeExtension(**kwargs):
    import markdown

    class DitaaExtension(markdown.Extension):
        def extendMarkdown(self, md):
            # Must run before SuperFences.
            md.preprocessors.register(
                DitaaFencePreprocessor(md),
                "ditaa_fence_preprocessor",
                35,
            )

    return DitaaExtension(**kwargs)