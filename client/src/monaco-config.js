import * as monaco from "monaco-editor";

self.MonacoEnvironment = {
    getWorkerUrl: function (_, label) {
        return new URL(
            `monaco-editor/esm/vs/editor/editor.worker.js`,
            import.meta.url
        ).toString();
    },
};
