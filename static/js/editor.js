document.addEventListener("DOMContentLoaded", function() {
    
    // 1. Initialize Split.js
    Split(['#editor-pane', '#output-pane'], {
        sizes: [50, 50], minSize: 300, gutterSize: 4, cursor: 'col-resize'
    });
    Split(['#code-output-pane', '#terminal-pane'], {
        direction: 'vertical', sizes: [70, 30], minSize: 100, gutterSize: 4, cursor: 'row-resize'
    });

    // 2. Visual Toggle Logic for the Optimizer Button
    const optToggle = document.getElementById('optimizeToggle');
    const toggleBg = document.getElementById('toggleBg');
    const toggleDot = document.getElementById('toggleDot');
    
    optToggle.addEventListener('change', (e) => {
        if(e.target.checked) {
            toggleBg.classList.replace('bg-gray-700', 'bg-blue-500');
            toggleDot.classList.replace('translate-x-0', 'translate-x-4');
        } else {
            toggleBg.classList.replace('bg-blue-500', 'bg-gray-700');
            toggleDot.classList.replace('translate-x-4', 'translate-x-0');
        }
    });

    // 3. Load Monaco Editor Safely
    if (typeof require === 'undefined') {
        document.getElementById('terminalContent').innerHTML = "<span class='text-red-500'>Error: Monaco Editor CDN blocked by browser.</span>";
        return;
    }

    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.30.1/min/vs' }});
    require(['vs/editor/editor.main'], function() {
        window.editor = monaco.editor.create(document.getElementById('editor'), {
            value: "mangaao math;\n\nmaan_lo x = 10 * 5;\n\n// Ye loop aur math optimizer check karega\nagar (x > 20) {\n    dikhao(\"Bhai, compiler is working!\");\n} warna {\n    dikhao(\"Dead code block eliminated.\");\n}",
            language: 'javascript', // Fallback to JS if custom language fails
            theme: 'vs-dark',
            automaticLayout: true,
            minimap: { enabled: false },
            fontSize: 15
        });

        // Add keyboard shortcut
        window.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, function() {
            document.getElementById('compileBtn').click();
        });
    });

    // 4. API Logic & Button Listeners
    let activeLang = 'python';

    document.querySelectorAll('.lang-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            document.querySelectorAll('.lang-tab').forEach(t => {
                t.classList.remove('border-blue-500', 'text-blue-400', 'active-tab');
                t.classList.add('border-transparent', 'text-gray-500');
            });
            const target = e.currentTarget;
            target.classList.remove('border-transparent', 'text-gray-500');
            target.classList.add('border-blue-500', 'text-blue-400', 'active-tab');
            activeLang = target.dataset.lang;
        });
    });

    function printToTerminal(text, type = 'info') {
        const term = document.getElementById('terminalContent');
        const colorClass = type === 'error' ? 'text-red-400' : (type === 'success' ? 'text-green-400' : 'text-gray-300');
        term.innerHTML += `<div class="mb-1 ${colorClass}">${text}</div>`;
        const pane = document.getElementById('terminal-pane').querySelector('.overflow-auto');
        pane.scrollTop = pane.scrollHeight;
    }

    document.getElementById('clearTerminal').addEventListener('click', () => {
        document.getElementById('terminalContent').innerHTML = '';
    });

    // COMPILE BUTTON LOGIC
    document.getElementById('compileBtn').addEventListener('click', async () => {
        if (!window.editor) {
            printToTerminal("Error: Editor not loaded yet.", "error");
            return;
        }

        const code = window.editor.getValue();
        const isOptimized = document.getElementById('optimizeToggle').checked; // GET TOGGLE STATE
        const outputArea = document.getElementById('outputCode');
        
        outputArea.textContent = `// Compiling to ${activeLang.toUpperCase()}...\n// Optimization: ${isOptimized ? 'ON' : 'OFF'}`;
        printToTerminal(`Compiling...`, 'info');

        try {
            const response = await fetch('/compile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    code: code, 
                    language: activeLang,
                    optimize: isOptimized // SEND TO FLASK
                })
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                outputArea.textContent = result.compiled_code;
                printToTerminal(`✔ Success`, 'success');
            } else {
                outputArea.textContent = "// Compilation Failed.";
                printToTerminal(`✖ ${result.console}`, 'error');
            }
        } catch (error) {
            printToTerminal(`✖ API Error: Cannot reach Flask Backend.`, 'error');
        }
    });
});