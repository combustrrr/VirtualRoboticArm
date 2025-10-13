"""Three.js asset helpers."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List


ASSET_ROOT = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "models"
    / "puma560_vlab_mirror"
    / "exp"
    / "forward-kinematics"
    / "simulation"
)


@lru_cache(maxsize=None)
def _load_asset(relative_path: str) -> str:
    return (ASSET_ROOT / relative_path).read_text(encoding="utf-8")


@lru_cache(maxsize=None)
def _sanitize_script(content: str) -> str:
    return content.replace("</script>", "<\\/script>")


@lru_cache(maxsize=1)
def _get_threejs_runtime() -> Dict[str, str]:
    return {
        "three": _load_asset("js/threejs/three.min.js"),
        "trackball": _load_asset("js/threejs/TrackballControls.js"),
        "detector": _load_asset("js/threejs/Detector.js"),
        "stats": _load_asset("js/threejs/stats.min.js"),
        "font_regular": _load_asset("fonts/droid_sans_regular.typeface.js"),
        "font_bold": _load_asset("fonts/droid_sans_bold.typeface.js"),
        "font_helvetiker_regular": _load_asset("fonts/helvetiker_regular.typeface.js"),
        "font_helvetiker_bold": _load_asset("fonts/helvetiker_bold.typeface.js"),
        "axis": _load_asset("js/axis.js"),
        "scene": _load_asset("js/PUMA_scene.js"),
    }


def _build_static_html_structure() -> List[str]:
    return [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '    <meta charset="utf-8" />',
        "    <style>",
        "        html, body { margin: 0; padding: 0; background: #000; }",
        "        #canvas3d-container { position: relative; width: 100%; height: 720px; }",
        "        #canvas3d-view { width: 100%; height: 100%; }",
        "        #loading {",
        "            position: absolute;",
        "            top: 50%;",
        "            left: 50%;",
        "            transform: translate(-50%, -50%);",
        "            color: #fff;",
        "            font-family: Arial, sans-serif;",
        "            z-index: 1000;",
        "            letter-spacing: 0.08em;",
        "        }",
        "    </style>",
        "</head>",
        "<body>",
        '    <div id="canvas3d-container">',
        '        <div id="loading">Loading 3D Model...</div>',
        '        <div id="canvas3d-view"></div>',
        '    </div>',
    ]


def _build_runtime_scripts(runtime: Dict[str, str]) -> List[str]:
    scripts: List[str] = []
    for key in [
        "three",
        "trackball",
        "detector",
        "stats",
        "font_regular",
        "font_bold",
        "font_helvetiker_regular",
        "font_helvetiker_bold",
        "axis",
        "scene",
    ]:
        scripts.append("    <script>")
        scripts.append(_sanitize_script(runtime[key]))
        scripts.append("    </script>")
    return scripts


def _build_viewer_script(angles_json: str) -> List[str]:
    return [
        "    <script>",
        f"        const JOINT_ANGLES = {angles_json};",
        "",
        "        function degToRad(degrees) {",
        "            return degrees * Math.PI / 180;",
        "        }",
        "",
        "        function applyJointAngles(angles) {",
        "            if (!window.PUMA560) {",
        "                return;",
        "            }",
        "            PUMA560.link2Mesh.rotation.y = degToRad(angles[0] || 0);",
        "            PUMA560.Link3Mesh.rotation.x = degToRad(angles[1] || 0);",
        "            PUMA560.Link4Mesh.rotation.x = degToRad(angles[2] || 0);",
        "            PUMA560.BoxL5.rotation.y = degToRad(angles[3] || 0);",
        "            PUMA560.Cylinder3L5.rotation.x = degToRad(angles[4] || 0);",
        "            PUMA560.CylinderL6.rotation.x = degToRad(angles[5] || 0);",
        "            if (typeof render === 'function') {",
        "                render();",
        "            }",
        "        }",
        "",
        "        function initializeViewer() {",
        "            if (typeof Detector !== 'undefined' && !Detector.webgl) {",
        "                document.body.innerHTML = '<p style=\"color:#fff;text-align:center;\">WebGL is not supported in this browser.</p>';",
        "                return;",
        "            }",
        "",
        "            if (window.PUMA560 && typeof PUMA560.init === 'function') {",
        "                PUMA560.init();",
        "                if (typeof animate === 'function') {",
        "                    animate();",
        "                }",
        "                applyJointAngles(JOINT_ANGLES);",
        "            }",
        "",
        "            const loadingEl = document.getElementById('loading');",
        "            if (loadingEl) {",
        "                loadingEl.style.display = 'none';",
        "            }",
        "        }",
        "",
        "        if (document.readyState === 'loading') {",
        "            document.addEventListener('DOMContentLoaded', initializeViewer);",
        "        } else {",
        "            initializeViewer();",
        "        }",
        "    </script>",
        "</body>",
        "</html>",
    ]


def build_threejs_html(joint_angles: Iterable[float]) -> str:
    """Compose the inline Three.js viewer HTML."""
    runtime = _get_threejs_runtime()
    angles_json = json.dumps(list(joint_angles))

    html_parts: List[str] = []
    html_parts.extend(_build_static_html_structure())
    html_parts.extend(_build_runtime_scripts(runtime))
    html_parts.extend(_build_viewer_script(angles_json))

    return "\n".join(html_parts)
