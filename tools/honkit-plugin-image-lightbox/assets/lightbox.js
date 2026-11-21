(function () {
    "use strict";

    if (window.__hjImageLightboxInit) {
        return;
    }
    window.__hjImageLightboxInit = true;

    var MIN_SCALE = 0.5;
    var MAX_SCALE = 4.0;

    var state = {
        images: [],
        currentIndex: -1,
        scale: 1,
        tx: 0,
        ty: 0,
        isDragging: false,
        dragMoved: false,
        suppressStageClick: false,
        pointerStartX: 0,
        pointerStartY: 0,
        startTx: 0,
        startTy: 0
    };

    var dom = null;

    function clamp(val, min, max) {
        return Math.max(min, Math.min(max, val));
    }

    function isEligibleImage(img) {
        if (!img || img.tagName !== "IMG") {
            return false;
        }
        if (img.classList.contains("no-lightbox")) {
            return false;
        }
        if (img.closest("a[href]")) {
            return false;
        }
        if (!img.complete || img.naturalWidth === 0) {
            return false;
        }
        return true;
    }

    function getPageImages() {
        var nodes = document.querySelectorAll(".markdown-section img");
        var list = [];
        for (var i = 0; i < nodes.length; i++) {
            if (isEligibleImage(nodes[i])) {
                list.push(nodes[i]);
            }
        }
        return list;
    }

    function ensureDom() {
        if (dom) {
            return dom;
        }

        var root = document.createElement("div");
        root.className = "hj-lightbox";
        root.setAttribute("role", "dialog");
        root.setAttribute("aria-modal", "true");
        root.setAttribute("aria-label", "图片放大预览");
        root.innerHTML = [
            '<div class="hj-lightbox-toolbar">',
            '  <div class="hj-lightbox-counter" aria-live="polite">1 / 1</div>',
            '  <div class="hj-lightbox-actions">',
            '    <button type="button" class="hj-lightbox-btn is-zoom-out" aria-label="缩小" title="缩小 (-)">−</button>',
            '    <button type="button" class="hj-lightbox-btn hj-lightbox-zoom-badge is-zoom-reset" aria-label="重置缩放" title="重置缩放 (0)">100%</button>',
            '    <button type="button" class="hj-lightbox-btn is-zoom-in" aria-label="放大" title="放大 (+)">+</button>',
            '    <button type="button" class="hj-lightbox-btn is-close" aria-label="关闭" title="关闭 (ESC)">×</button>',
            "  </div>",
            "</div>",
            '<div class="hj-lightbox-stage">',
            '  <button type="button" class="hj-lightbox-nav is-prev" aria-label="上一张" title="上一张 (←)">‹</button>',
            '  <img class="hj-lightbox-img" alt="" draggable="false" />',
            '  <button type="button" class="hj-lightbox-nav is-next" aria-label="下一张" title="下一张 (→)">›</button>',
            "</div>",
            '<div class="hj-lightbox-footer">',
            '  <div class="hj-lightbox-caption is-empty"></div>',
            '  <div class="hj-lightbox-hint">滚轮缩放 · 双击放大 · ESC 关闭</div>',
            "</div>"
        ].join("");

        document.body.appendChild(root);

        dom = {
            root: root,
            counter: root.querySelector(".hj-lightbox-counter"),
            zoomOutBtn: root.querySelector(".is-zoom-out"),
            zoomResetBtn: root.querySelector(".is-zoom-reset"),
            zoomInBtn: root.querySelector(".is-zoom-in"),
            closeBtn: root.querySelector(".is-close"),
            stage: root.querySelector(".hj-lightbox-stage"),
            prevBtn: root.querySelector(".is-prev"),
            nextBtn: root.querySelector(".is-next"),
            img: root.querySelector(".hj-lightbox-img"),
            caption: root.querySelector(".hj-lightbox-caption")
        };

        bindOverlayEvents();
        return dom;
    }

    function applyTransform() {
        if (!dom) {
            return;
        }
        dom.img.style.transform =
            "translate3d(" + state.tx + "px, " + state.ty + "px, 0) scale(" + state.scale + ")";
        dom.zoomResetBtn.textContent = Math.round(state.scale * 100) + "%";
        if (state.scale > 1.01) {
            dom.img.classList.add("is-zoomed");
        } else {
            dom.img.classList.remove("is-zoomed");
        }
    }

    function setScale(nextScale) {
        var clamped = clamp(Math.round(nextScale * 100) / 100, MIN_SCALE, MAX_SCALE);
        state.scale = clamped;
        if (state.scale <= 1) {
            state.tx = 0;
            state.ty = 0;
        }
        applyTransform();
    }

    function resetView() {
        state.scale = 1;
        state.tx = 0;
        state.ty = 0;
        applyTransform();
    }

    function showImageAt(index) {
        if (!state.images.length) {
            return;
        }
        var total = state.images.length;
        state.currentIndex = ((index % total) + total) % total;

        var sourceImg = state.images[state.currentIndex];
        var d = ensureDom();

        resetView();
        d.img.src = sourceImg.currentSrc || sourceImg.src;
        var altText = (sourceImg.getAttribute("alt") || sourceImg.getAttribute("title") || "").trim();
        d.img.alt = altText;
        d.caption.textContent = altText;
        if (altText) {
            d.caption.classList.remove("is-empty");
        } else {
            d.caption.classList.add("is-empty");
        }

        d.counter.textContent = (state.currentIndex + 1) + " / " + total;
        if (total <= 1) {
            d.root.classList.add("is-single");
        } else {
            d.root.classList.remove("is-single");
        }
    }

    function openLightbox(images, index) {
        if (!images || !images.length) {
            return;
        }
        state.images = images;
        var d = ensureDom();
        showImageAt(index);
        d.root.classList.add("is-open");
        document.body.classList.add("hj-lightbox-lock");
    }

    function closeLightbox() {
        if (!dom || !dom.root.classList.contains("is-open")) {
            return;
        }
        dom.root.classList.remove("is-open");
        dom.img.classList.remove("is-dragging");
        document.body.classList.remove("hj-lightbox-lock");
        state.isDragging = false;
        state.dragMoved = false;
        state.suppressStageClick = false;
    }

    function isOpen() {
        return Boolean(dom && dom.root.classList.contains("is-open"));
    }

    function bindOverlayEvents() {
        dom.closeBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            closeLightbox();
        });

        dom.zoomInBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            setScale(state.scale + 0.25);
        });

        dom.zoomOutBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            setScale(state.scale - 0.25);
        });

        dom.zoomResetBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            resetView();
        });

        dom.prevBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            showImageAt(state.currentIndex - 1);
        });

        dom.nextBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            showImageAt(state.currentIndex + 1);
        });

        dom.stage.addEventListener("click", function (e) {
            if (state.suppressStageClick) {
                state.suppressStageClick = false;
                return;
            }
            if (e.target === dom.stage) {
                closeLightbox();
            }
        });

        dom.root.addEventListener("click", function (e) {
            if (e.target === dom.root || e.target.classList.contains("hj-lightbox-toolbar") || e.target.classList.contains("hj-lightbox-footer")) {
                closeLightbox();
            }
        });

        dom.img.addEventListener("dblclick", function (e) {
            e.preventDefault();
            e.stopPropagation();
            if (state.scale > 1.01) {
                resetView();
            } else {
                setScale(2);
            }
        });

        dom.stage.addEventListener(
            "wheel",
            function (e) {
                if (!isOpen()) {
                    return;
                }
                e.preventDefault();
                var delta = e.deltaY < 0 ? 0.2 : -0.2;
                setScale(state.scale + delta);
            },
            { passive: false }
        );

        dom.img.addEventListener("mousedown", function (e) {
            if (e.button !== 0 || state.scale <= 1.01) {
                return;
            }
            e.preventDefault();
            state.isDragging = true;
            state.dragMoved = false;
            state.pointerStartX = e.clientX;
            state.pointerStartY = e.clientY;
            state.startTx = state.tx;
            state.startTy = state.ty;
            dom.img.classList.add("is-dragging");
        });

        document.addEventListener("mousemove", function (e) {
            if (!state.isDragging) {
                return;
            }
            var dx = e.clientX - state.pointerStartX;
            var dy = e.clientY - state.pointerStartY;
            if (Math.abs(dx) > 4 || Math.abs(dy) > 4) {
                state.dragMoved = true;
            }
            state.tx = state.startTx + dx;
            state.ty = state.startTy + dy;
            applyTransform();
        });

        document.addEventListener("mouseup", function () {
            if (!state.isDragging) {
                return;
            }
            state.isDragging = false;
            if (dom) {
                dom.img.classList.remove("is-dragging");
            }
            if (state.dragMoved) {
                state.suppressStageClick = true;
                setTimeout(function () {
                    state.suppressStageClick = false;
                }, 0);
            }
        });
    }

    document.addEventListener("click", function (e) {
        var target = e.target;
        if (!target || target.tagName !== "IMG") {
            return;
        }
        if (!target.closest(".markdown-section")) {
            return;
        }
        if (!isEligibleImage(target)) {
            return;
        }
        e.preventDefault();
        var pageImages = getPageImages();
        var idx = pageImages.indexOf(target);
        if (idx === -1) {
            pageImages = [target];
            idx = 0;
        }
        openLightbox(pageImages, idx);
    });

    document.addEventListener("keydown", function (e) {
        if (!isOpen()) {
            return;
        }
        if (e.key === "Escape") {
            e.preventDefault();
            closeLightbox();
        } else if (e.key === "ArrowLeft") {
            if (state.images.length > 1) {
                e.preventDefault();
                showImageAt(state.currentIndex - 1);
            }
        } else if (e.key === "ArrowRight") {
            if (state.images.length > 1) {
                e.preventDefault();
                showImageAt(state.currentIndex + 1);
            }
        } else if (e.key === "+" || e.key === "=") {
            e.preventDefault();
            setScale(state.scale + 0.25);
        } else if (e.key === "-" || e.key === "_") {
            e.preventDefault();
            setScale(state.scale - 0.25);
        } else if (e.key === "0") {
            e.preventDefault();
            resetView();
        }
    });

    function bindGitbookEvents() {
        if (window.gitbook && window.gitbook.events && typeof window.gitbook.events.bind === "function") {
            window.gitbook.events.bind("page.change", function () {
                closeLightbox();
            });
            return true;
        }
        return false;
    }

    if (!bindGitbookEvents() && typeof window.require === "function") {
        try {
            window.require(["gitbook"], function (gitbook) {
                if (gitbook && gitbook.events && typeof gitbook.events.bind === "function") {
                    gitbook.events.bind("page.change", function () {
                        closeLightbox();
                    });
                }
            });
        } catch (err) {
            // Ignore if AMD loader is not active
        }
    }
})();
