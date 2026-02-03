"""
Finite Automata Toolkit - Streamlit Arayüzü
"""
import streamlit as st
import json
import os
from automata import NFA, DFA, AutomataVisualizer
from automata.lazy_subset import LazySubsetConstruction
from automata.minimization import DFAMinimization
from automata.regex_to_nfa import RegexToNFA
from automata.comparison import DFAComparison

# Sayfa yapılandırması
st.set_page_config(
    page_title="Finite Automata Toolkit",
    page_icon="🔄",
    layout="wide"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Visualizer başlat
visualizer = AutomataVisualizer()


def show_nfa_graph(nfa: NFA, title: str = "NFA", highlight_states=None):
    """NFA grafiğini göster"""
    graph = visualizer.visualize_nfa(
        nfa.states, nfa.alphabet, nfa.transitions,
        nfa.start_state, nfa.accept_states,
        title=title,
        highlight_states=highlight_states
    )
    st.graphviz_chart(graph.source)


def show_dfa_graph(dfa: DFA, title: str = "DFA", state_labels=None, highlight_states=None):
    """DFA grafiğini göster"""
    graph = visualizer.visualize_dfa(
        dfa.states, dfa.alphabet, dfa.transitions,
        dfa.start_state, dfa.accept_states,
        title=title,
        state_labels=state_labels,
        highlight_states=highlight_states
    )
    st.graphviz_chart(graph.source)


def parse_nfa_input(json_str: str) -> NFA:
    """JSON string'den NFA oluştur"""
    data = json.loads(json_str)
    return NFA.from_json(data)


def parse_dfa_input(json_str: str) -> DFA:
    """JSON string'den DFA oluştur"""
    data = json.loads(json_str)
    return DFA.from_json(data)


# Ana başlık
st.markdown('<h1 class="main-header">🔄 Finite Automata Toolkit</h1>', unsafe_allow_html=True)

# Sidebar menü
st.sidebar.title("📋 Menü")
menu_option = st.sidebar.radio(
    "İşlem Seçin:",
    [
        "🏠 Ana Sayfa",
        "🎨 JSON Creator (GUI)",
        "1️⃣ NFA → DFA (Lazy Subset)",
        "2️⃣ DFA Minimization",
        "3️⃣ Regex → ε-NFA",
        "4️⃣ DFA Karşılaştırma"
    ]
)

# Örnek NFA JSON
EXAMPLE_NFA = """{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a", "b"],
  "transitions": {
    "q0": {"a": ["q0", "q1"], "b": ["q0"]},
    "q1": {"b": ["q2"]},
    "q2": {}
  },
  "start_state": "q0",
  "accept_states": ["q2"]
}"""

EXAMPLE_NFA_EPSILON = """{
  "states": ["q0", "q1", "q2", "q3"],
  "alphabet": ["a", "b"],
  "transitions": {
    "q0": {"ε": ["q1"], "a": ["q0"]},
    "q1": {"b": ["q2"]},
    "q2": {"ε": ["q3"]},
    "q3": {}
  },
  "start_state": "q0",
  "accept_states": ["q3"]
}"""

EXAMPLE_DFA = """{
  "states": ["q0", "q1", "q2", "q3", "q4"],
  "alphabet": ["a", "b"],
  "transitions": {
    "q0": {"a": "q1", "b": "q2"},
    "q1": {"a": "q1", "b": "q3"},
    "q2": {"a": "q1", "b": "q2"},
    "q3": {"a": "q1", "b": "q4"},
    "q4": {"a": "q1", "b": "q2"}
  },
  "start_state": "q0",
  "accept_states": ["q4"]
}"""


# ==================== ANA SAYFA ====================
if menu_option == "🏠 Ana Sayfa":
    st.markdown("""
    ## Hoş Geldiniz! 👋
    
    Bu uygulama, sonlu otomatlar (Finite Automata) üzerinde çeşitli işlemler yapmanızı sağlar.
    
    ### 📚 Özellikler
    
    | Modül | Açıklama |
    |-------|----------|
    | **NFA → DFA (Lazy Subset)** | Lazy Subset Construction algoritması ile NFA'yı DFA'ya dönüştürür |
    | **DFA Minimization** | Table-Filling algoritması ile DFA'yı minimize eder |
    | **Regex → ε-NFA** | Thompson Construction ile regex'i ε-NFA'ya dönüştürür |
    | **DFA Karşılaştırma** | İki DFA'nın eşdeğerliğini kontrol eder |
    
    ### 📝 JSON Formatı
    
    NFA ve DFA'lar aşağıdaki JSON formatında tanımlanır:
    
    ```json
    {
      "states": ["q0", "q1", "q2"],
      "alphabet": ["a", "b"],
      "transitions": {
        "q0": {"a": ["q0", "q1"], "b": ["q0"]},
        "q1": {"b": ["q2"]},
        "q2": {}
      },
      "start_state": "q0",
      "accept_states": ["q2"]
    }
    ```
    
    **Not:** Epsilon geçişleri için `"ε"` sembolünü kullanın.
    
    ---
    👈 Sol menüden bir işlem seçerek başlayın!
    """)
    
    st.info("💡 **İpucu:** Her modülde örnek giriş verileri mevcuttur. 'Örnek Yükle' butonunu kullanabilirsiniz.")


# ==================== JSON CREATOR (GUI) ====================
elif menu_option == "🎨 JSON Creator (GUI)":
    st.header("🎨 Finite Automata JSON Creator")
    
    st.markdown("""
    **Grafik arayüz ile finite automata oluşturun!**
    
    Bu araç ile GUI kullanarak NFA veya DFA tanımlayabilir ve JSON formatında çıktı alabilirsiniz.
    Oluşturulan JSON'u diğer modüllerde kullanabilirsiniz.
    """)
    
    # Initialize session state for the automata builder
    if 'gui_states' not in st.session_state:
        st.session_state.gui_states = ['q0']
    if 'gui_alphabet' not in st.session_state:
        st.session_state.gui_alphabet = []
    if 'gui_transitions' not in st.session_state:
        st.session_state.gui_transitions = {}
    if 'gui_start_state' not in st.session_state:
        st.session_state.gui_start_state = 'q0'
    if 'gui_accept_states' not in st.session_state:
        st.session_state.gui_accept_states = []
    if 'gui_state_queue' not in st.session_state:
        st.session_state.gui_state_queue = ['q0']
    if 'gui_processed_states' not in st.session_state:
        st.session_state.gui_processed_states = []
    if 'gui_automata_type' not in st.session_state:
        st.session_state.gui_automata_type = 'NFA'
    
    # Automata type selection
    st.subheader("1️⃣ Select Automata Type")
    automata_type = st.radio(
        "Choose the type of automata:",
        ["NFA", "DFA"],
        horizontal=True,
        key="automata_type_radio"
    )
    st.session_state.gui_automata_type = automata_type
    
    # Alphabet definition
    st.subheader("2️⃣ Define Alphabet")
    col1, col2 = st.columns([3, 1])
    with col1:
        alphabet_input = st.text_input(
            "Enter alphabet symbols (comma-separated):",
            value=", ".join(st.session_state.gui_alphabet) if st.session_state.gui_alphabet else "a, b",
            key="alphabet_input"
        )
    with col2:
        if st.button("Set Alphabet", type="primary"):
            new_alphabet = [s.strip() for s in alphabet_input.split(',') if s.strip()]
            st.session_state.gui_alphabet = new_alphabet
            st.success(f"✅ Alphabet set: {{{', '.join(new_alphabet)}}}")
    
    # Display current alphabet
    if st.session_state.gui_alphabet:
        st.info(f"**Current Alphabet:** {{{', '.join(st.session_state.gui_alphabet)}}}")
    
    # Start state configuration
    st.subheader("3️⃣ Configure Start State")
    col1, col2 = st.columns([3, 1])
    with col1:
        start_state_input = st.text_input(
            "Start state:",
            value=st.session_state.gui_start_state,
            key="start_state_input"
        )
    with col2:
        if st.button("Set Start State"):
            st.session_state.gui_start_state = start_state_input
            if start_state_input not in st.session_state.gui_states:
                st.session_state.gui_states.append(start_state_input)
            if start_state_input not in st.session_state.gui_state_queue:
                st.session_state.gui_state_queue.append(start_state_input)
            st.success(f"✅ Start state set: {start_state_input}")
    
    st.info(f"**Current Start State:** {st.session_state.gui_start_state}")
    
    # State queue and transition builder
    st.subheader("4️⃣ Build Transitions")
    
    st.markdown("""
    **How it works:**
    1. States are processed from the queue one by one
    2. For each state, define transitions for each alphabet symbol
    3. New states introduced in transitions are automatically added to the queue
    4. Process continues until all states in the queue are processed
    """)
    
    # Display queue status
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📋 State Queue (to be processed):**")
        if st.session_state.gui_state_queue:
            for state in st.session_state.gui_state_queue:
                st.write(f"- {state}")
        else:
            st.write("*Queue is empty*")
    
    with col2:
        st.markdown("**✅ Processed States:**")
        if st.session_state.gui_processed_states:
            for state in st.session_state.gui_processed_states:
                st.write(f"- {state}")
        else:
            st.write("*No states processed yet*")
    
    # Process next state from queue
    if st.session_state.gui_state_queue and st.session_state.gui_alphabet:
        st.divider()
        current_state = st.session_state.gui_state_queue[0]
        st.markdown(f"### 🔵 Processing State: **{current_state}**")
        
        # Initialize transitions for current state if not exists
        if current_state not in st.session_state.gui_transitions:
            st.session_state.gui_transitions[current_state] = {}
        
        # Build transitions for current state
        st.markdown("**Define outgoing transitions:**")
        
        temp_transitions = {}
        all_symbols = st.session_state.gui_alphabet.copy()
        if automata_type == "NFA":
            all_symbols.append("ε")  # Add epsilon for NFA
        
        cols = st.columns(len(all_symbols))
        for idx, symbol in enumerate(all_symbols):
            with cols[idx]:
                st.markdown(f"**δ({current_state}, {symbol})**")
                
                # Get existing transition if any
                existing = st.session_state.gui_transitions[current_state].get(symbol, [])
                if isinstance(existing, str):
                    existing = [existing]
                existing_str = ", ".join(existing) if existing else ""
                
                target_input = st.text_input(
                    f"Target state(s):",
                    value=existing_str,
                    key=f"trans_{current_state}_{symbol}",
                    placeholder="q1, q2" if automata_type == "NFA" else "q1"
                )
                
                if target_input.strip():
                    targets = [t.strip() for t in target_input.split(',') if t.strip()]
                    
                    # For DFA, only allow one target state
                    if automata_type == "DFA" and len(targets) > 1:
                        st.error(f"⚠️ DFA allows only one target state per symbol. Please enter a single state.")
                        continue  # Skip this transition
                    
                    # For DFA, ensure we have exactly one target
                    if automata_type == "DFA":
                        if len(targets) == 1:
                            temp_transitions[symbol] = targets[0]
                        # else: skip empty targets for DFA
                    else:
                        # For NFA, store as list
                        temp_transitions[symbol] = targets
                    
                    # Add new states to queue and states list
                    for target in targets:
                        if target not in st.session_state.gui_states:
                            st.session_state.gui_states.append(target)
                        if target not in st.session_state.gui_state_queue and target not in st.session_state.gui_processed_states:
                            st.session_state.gui_state_queue.append(target)
        
        # Save and move to next state
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Save Transitions & Process Next State", type="primary"):
                # Save transitions for current state
                st.session_state.gui_transitions[current_state] = temp_transitions
                
                # Move current state from queue to processed
                st.session_state.gui_processed_states.append(current_state)
                st.session_state.gui_state_queue.pop(0)
                
                st.success(f"✅ Transitions saved for {current_state}")
                st.rerun()
        
        with col2:
            if st.button("⏭️ Skip State"):
                # Move to next without saving
                st.session_state.gui_processed_states.append(current_state)
                st.session_state.gui_state_queue.pop(0)
                st.rerun()
    
    elif st.session_state.gui_alphabet and not st.session_state.gui_state_queue:
        st.success("✅ All states processed!")
    
    # Accept states configuration
    st.divider()
    st.subheader("5️⃣ Define Accept States")
    
    if st.session_state.gui_states:
        st.markdown("Select which states are accept (final) states:")
        
        accept_states_selected = []
        cols = st.columns(min(len(st.session_state.gui_states), 5))
        for idx, state in enumerate(st.session_state.gui_states):
            with cols[idx % len(cols)]:
                is_accept = st.checkbox(
                    state,
                    value=state in st.session_state.gui_accept_states,
                    key=f"accept_{state}"
                )
                if is_accept:
                    accept_states_selected.append(state)
        
        if st.button("Save Accept States"):
            st.session_state.gui_accept_states = accept_states_selected
            st.success(f"✅ Accept states: {{{', '.join(accept_states_selected)}}}")
        
        if st.session_state.gui_accept_states:
            st.info(f"**Current Accept States:** {{{', '.join(st.session_state.gui_accept_states)}}}")
    
    # Generate JSON output
    st.divider()
    st.subheader("6️⃣ Generated JSON Output")
    
    if st.button("🔄 Generate JSON", type="primary"):
        # Build the JSON structure
        json_output = {
            "states": st.session_state.gui_states,
            "alphabet": st.session_state.gui_alphabet,
            "transitions": {},
            "start_state": st.session_state.gui_start_state,
            "accept_states": st.session_state.gui_accept_states
        }
        
        # Format transitions based on automata type
        for state, trans in st.session_state.gui_transitions.items():
            json_output["transitions"][state] = {}
            for symbol, targets in trans.items():
                if automata_type == "NFA":
                    # For NFA, ensure targets is a list
                    if isinstance(targets, str):
                        json_output["transitions"][state][symbol] = [targets]
                    else:
                        json_output["transitions"][state][symbol] = targets
                else:
                    # For DFA, ensure target is a string
                    if isinstance(targets, list):
                        if targets:  # Only add transition if there's a target
                            json_output["transitions"][state][symbol] = targets[0]
                        # else: skip empty transitions
                    else:
                        json_output["transitions"][state][symbol] = targets
        
        # Add empty transitions for states not yet processed
        for state in st.session_state.gui_states:
            if state not in json_output["transitions"]:
                json_output["transitions"][state] = {}
        
        st.session_state.gui_json_output = json_output
    
    # Display JSON output
    if 'gui_json_output' in st.session_state:
        json_str = json.dumps(st.session_state.gui_json_output, indent=2, ensure_ascii=False)
        
        st.markdown("**✨ Your Finite Automata JSON:**")
        st.code(json_str, language="json")
        
        # Download button
        st.download_button(
            label="⬇️ Download JSON",
            data=json_str,
            file_name=f"{automata_type.lower()}_created.json",
            mime="application/json"
        )
        
        # Visualize the created automata
        st.divider()
        st.subheader("📊 Automata Visualization")
        
        try:
            if automata_type == "NFA":
                # Convert to NFA object and visualize
                nfa = NFA.from_json(st.session_state.gui_json_output)
                show_nfa_graph(nfa, f"Created {automata_type}")
            else:
                # Convert to DFA object and visualize
                dfa = DFA.from_json(st.session_state.gui_json_output)
                show_dfa_graph(dfa, f"Created {automata_type}")
            
            st.success("✅ Automata is valid and visualized!")
        except Exception as e:
            st.error(f"❌ Error in automata: {e}")
    
    # Reset button
    st.divider()
    if st.button("🔄 Reset and Start Over"):
        st.session_state.gui_states = ['q0']
        st.session_state.gui_alphabet = []
        st.session_state.gui_transitions = {}
        st.session_state.gui_start_state = 'q0'
        st.session_state.gui_accept_states = []
        st.session_state.gui_state_queue = ['q0']
        st.session_state.gui_processed_states = []
        if 'gui_json_output' in st.session_state:
            del st.session_state.gui_json_output
        st.rerun()


# ==================== LAZY SUBSET CONSTRUCTION ====================
elif menu_option == "1️⃣ NFA → DFA (Lazy Subset)":
    st.header("🔄 NFA → DFA (Lazy Subset Construction)")
    
    st.markdown("""
    **Lazy Subset Construction** algoritması, NFA'yı DFA'ya dönüştürür.
    Normal subset construction'dan farkı, sadece gereken durumları "lazy" (tembel) olarak hesaplamasıdır.
    """)
    
    # Giriş seçenekleri
    input_method = st.radio("Giriş Yöntemi:", ["JSON Editör", "Dosya Yükle", "İnteraktif Oluştur"])
    
    nfa = None
    
    if input_method == "JSON Editör":
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("📋 Örnek NFA Yükle"):
                st.session_state['nfa_json'] = EXAMPLE_NFA
            if st.button("📋 Epsilon NFA Örneği"):
                st.session_state['nfa_json'] = EXAMPLE_NFA_EPSILON
            
            nfa_json = st.text_area(
                "NFA JSON:",
                value=st.session_state.get('nfa_json', EXAMPLE_NFA),
                height=300
            )
        
        with col2:
            try:
                nfa = parse_nfa_input(nfa_json)
                st.success("✅ NFA başarıyla yüklendi!")
                show_nfa_graph(nfa, "Giriş NFA")
            except Exception as e:
                st.error(f"❌ JSON hatası: {e}")
    
    elif input_method == "Dosya Yükle":
        uploaded_file = st.file_uploader("JSON dosyası seçin", type=['json'])
        if uploaded_file:
            try:
                content = uploaded_file.read().decode('utf-8')
                nfa = parse_nfa_input(content)
                st.success("✅ NFA başarıyla yüklendi!")
                show_nfa_graph(nfa, "Giriş NFA")
            except Exception as e:
                st.error(f"❌ Dosya hatası: {e}")
    
    else:  # İnteraktif
        st.subheader("İnteraktif NFA Oluşturucu")
        
        col1, col2 = st.columns(2)
        with col1:
            states_input = st.text_input("Durumlar (virgülle ayırın):", "q0, q1, q2")
            alphabet_input = st.text_input("Alfabe (virgülle ayırın):", "a, b")
            start_state = st.text_input("Başlangıç durumu:", "q0")
            accept_input = st.text_input("Kabul durumları (virgülle ayırın):", "q2")
        
        states = [s.strip() for s in states_input.split(',')]
        alphabet = [s.strip() for s in alphabet_input.split(',')]
        accept_states = [s.strip() for s in accept_input.split(',')]
        
        st.subheader("Geçişleri Tanımla")
        transitions = {}
        
        for state in states:
            transitions[state] = {}
            cols = st.columns(len(alphabet) + 1)  # +1 for epsilon
            
            for i, symbol in enumerate(alphabet + ['ε']):
                with cols[i]:
                    targets = st.text_input(
                        f"δ({state}, {symbol}):",
                        key=f"trans_{state}_{symbol}",
                        placeholder="q1, q2"
                    )
                    if targets.strip():
                        transitions[state][symbol] = set(t.strip() for t in targets.split(','))
        
        if st.button("NFA Oluştur"):
            try:
                nfa = NFA(
                    set(states),
                    set(alphabet),
                    transitions,
                    start_state,
                    set(accept_states)
                )
                st.session_state['interactive_nfa'] = nfa
                st.success("✅ NFA oluşturuldu!")
            except Exception as e:
                st.error(f"❌ Hata: {e}")
        
        if 'interactive_nfa' in st.session_state:
            nfa = st.session_state['interactive_nfa']
            show_nfa_graph(nfa, "Oluşturulan NFA")
    
    # Dönüşüm
    if nfa:
        st.divider()
        st.subheader("🔄 Subset Construction")
        
        if st.button("▶️ Dönüşümü Başlat", type="primary"):
            converter = LazySubsetConstruction(nfa)
            
            # Adım adım göster
            step_container = st.container()
            progress_bar = st.progress(0)
            
            steps = list(converter.convert_full())
            total_steps = len(steps)
            
            for i, step in enumerate(steps):
                progress_bar.progress((i + 1) / total_steps)
                
                with step_container:
                    with st.expander(f"Adım {step.get('step', i)}: {step['type']}", expanded=(i == len(steps)-1)):
                        st.markdown(f"```\n{step['description']}\n```")
                        
                        if step['type'] != 'init':
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**NFA (vurgulanan: mevcut durumlar)**")
                                highlight = step.get('from_nfa_states', set())
                                show_nfa_graph(nfa, f"NFA - Adım {step.get('step', i)}", highlight)
                            
                            with col2:
                                st.markdown("**DFA (oluşturulan)**")
                                current_dfa = DFA(
                                    step['current_dfa_states'],
                                    nfa.alphabet,
                                    step['current_dfa_transitions'],
                                    converter.dfa_start_state,
                                    step['current_dfa_accept'],
                                    converter.state_mapping
                                )
                                state_labels = {s: '{' + ','.join(sorted(converter.state_mapping.get(s, set()))) + '}' 
                                              for s in step['current_dfa_states']}
                                show_dfa_graph(current_dfa, f"DFA - Adım {step.get('step', i)}", state_labels)
            
            # Final sonuç
            st.divider()
            st.subheader("✅ Final DFA")
            
            final_dfa = converter.get_dfa()
            state_labels = {s: '{' + ','.join(sorted(converter.state_mapping.get(s, set()))) + '}' 
                          for s in final_dfa.states}
            show_dfa_graph(final_dfa, "Final DFA", state_labels)
            
            # JSON çıktısı
            with st.expander("📄 DFA JSON Çıktısı"):
                st.json(final_dfa.to_json())
            
            # İndirme butonu
            dfa_json = json.dumps(final_dfa.to_json(), indent=2, ensure_ascii=False)
            st.download_button(
                "⬇️ DFA'yı İndir (JSON)",
                dfa_json,
                "dfa_output.json",
                "application/json"
            )


# ==================== DFA MINIMIZATION ====================
elif menu_option == "2️⃣ DFA Minimization":
    st.header("📉 DFA Minimization")
    
    st.markdown("""
    **Table-Filling** (Myhill-Nerode) algoritması ile DFA minimizasyonu.
    Ayırt edilemeyen durumları birleştirerek minimal DFA oluşturur.
    """)
    
    # Giriş
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("📋 Örnek DFA Yükle"):
            st.session_state['dfa_json'] = EXAMPLE_DFA
        
        dfa_json = st.text_area(
            "DFA JSON:",
            value=st.session_state.get('dfa_json', EXAMPLE_DFA),
            height=300
        )
    
    dfa = None
    with col2:
        try:
            dfa = parse_dfa_input(dfa_json)
            st.success(f"✅ DFA yüklendi! ({len(dfa.states)} durum)")
            show_dfa_graph(dfa, "Giriş DFA")
        except Exception as e:
            st.error(f"❌ JSON hatası: {e}")
    
    if dfa:
        st.divider()
        st.subheader("📉 Minimizasyon")
        
        if st.button("▶️ Minimizasyonu Başlat", type="primary"):
            minimizer = DFAMinimization(dfa)
            
            step_container = st.container()
            progress_bar = st.progress(0)
            
            steps = list(minimizer.minimize_full())
            total_steps = len(steps)
            
            for i, step in enumerate(steps):
                progress_bar.progress((i + 1) / total_steps)
                
                with step_container:
                    with st.expander(f"Adım {step['step']}: {step['type']}", expanded=(i == len(steps)-1)):
                        st.markdown(f"```\n{step['description']}\n```")
                        
                        # Partition görselleştirmesi
                        if 'partition' in step:
                            partition = step['partition']
                            
                            # Renkli durumlar
                            colors = ['🔵', '🟢', '🟡', '🟠', '🔴', '🟣', '⚪', '🟤']
                            partition_display = []
                            for j, group in enumerate(partition):
                                color = colors[j % len(colors)]
                                partition_display.append(f"{color} {{{', '.join(sorted(group))}}}")
                            
                            st.markdown("**Partition:** " + " | ".join(partition_display))
                            
                            # Grafik
                            graph = visualizer.visualize_minimization_step(
                                minimizer.dfa.states,
                                minimizer.dfa.alphabet,
                                minimizer.dfa.transitions,
                                minimizer.dfa.start_state,
                                minimizer.dfa.accept_states,
                                partition,
                                step['step']
                            )
                            st.graphviz_chart(graph.source)
                        
                        # Tablo gösterimi
                        if step['type'] in ['base_case', 'iteration', 'final']:
                            st.markdown("**📊 Ayırt Edilebilirlik Tablosu:**")
                            st.text(minimizer.get_table_display())
            
            # Final sonuç
            st.divider()
            st.subheader("✅ Minimize Edilmiş DFA")
            
            minimized_dfa = minimizer._build_minimized_dfa()
            show_dfa_graph(minimized_dfa, "Minimize Edilmiş DFA")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Orijinal Durum Sayısı", len(dfa.states))
            with col2:
                st.metric("Minimize Durum Sayısı", len(minimized_dfa.states))
            
            # JSON çıktısı
            with st.expander("📄 Minimize DFA JSON"):
                st.json(minimized_dfa.to_json())
            
            dfa_json = json.dumps(minimized_dfa.to_json(), indent=2, ensure_ascii=False)
            st.download_button(
                "⬇️ Minimize DFA'yı İndir",
                dfa_json,
                "minimized_dfa.json",
                "application/json"
            )


# ==================== REGEX TO NFA ====================
elif menu_option == "3️⃣ Regex → ε-NFA":
    st.header("🔤 Regex → ε-NFA (Thompson Construction)")
    
    st.markdown("""
    **Thompson Construction** algoritması ile regular expression'ı ε-NFA'ya dönüştürür.
    
    ### Desteklenen Operatörler
    | Operatör | Açıklama | Örnek |
    |----------|----------|-------|
    | `ab` | Concatenation | `ab` → "a" ardından "b" |
    | `a\|b` | Union | `a\|b` → "a" veya "b" |
    | `a*` | Kleene Star | `a*` → 0 veya daha fazla "a" |
    | `a+` | Kleene Plus | `a+` → 1 veya daha fazla "a" |
    | `a?` | Optional | `a?` → 0 veya 1 "a" |
    | `(ab)` | Grouping | `(ab)*` → "ab" tekrarı |
    """)
    
    # Regex giriş
    col1, col2 = st.columns([2, 1])
    
    with col1:
        regex = st.text_input("Regular Expression:", value="(a|b)*abb")
    
    with col2:
        st.markdown("**Örnekler:**")
        examples = ["a*b", "(a|b)*", "a+b?", "(ab)*", "(a|b)*abb"]
        for ex in examples:
            if st.button(ex, key=f"regex_{ex}"):
                st.session_state['regex_input'] = ex
                st.rerun()
    
    if 'regex_input' in st.session_state:
        regex = st.session_state['regex_input']
    
    if regex:
        st.divider()
        st.subheader("🔄 Thompson Construction")
        
        if st.button("▶️ Dönüşümü Başlat", type="primary"):
            converter = RegexToNFA()
            
            step_container = st.container()
            progress_bar = st.progress(0)
            
            steps = list(converter.convert_full(regex))
            total_steps = len(steps)
            
            for i, step in enumerate(steps):
                progress_bar.progress((i + 1) / total_steps)
                
                with step_container:
                    with st.expander(f"Adım {step['step']}: {step['type']}", expanded=(i == len(steps)-1)):
                        st.markdown(f"```\n{step['description']}\n```")
                        
                        if step['type'] not in ['init', 'final']:
                            # Bu adımın NFA'sını görselleştir
                            graph = visualizer.visualize_nfa(
                                step['nfa_states'],
                                set(),
                                step['nfa_transitions'],
                                step['nfa_start'],
                                {step['nfa_accept']},
                                title=f"{step['type']} - Adım {step['step']}"
                            )
                            st.graphviz_chart(graph.source)
            
            # Final NFA
            st.divider()
            st.subheader("✅ Final ε-NFA")
            
            final_nfa = converter._final_nfa
            show_nfa_graph(final_nfa, f"ε-NFA for: {regex}")
            
            st.info(f"📊 Toplam {len(final_nfa.states)} durum, Alfabe: {final_nfa.alphabet}")
            
            # Test
            st.subheader("🧪 String Test")
            test_string = st.text_input("Test edilecek string:", "abb")
            if st.button("Test Et"):
                result = final_nfa.accepts(test_string)
                if result:
                    st.success(f"✅ '{test_string}' KABUL EDİLDİ")
                else:
                    st.error(f"❌ '{test_string}' REDDEDİLDİ")
            
            # JSON çıktısı
            with st.expander("📄 ε-NFA JSON"):
                st.json(final_nfa.to_json())
            
            nfa_json = json.dumps(final_nfa.to_json(), indent=2, ensure_ascii=False)
            st.download_button(
                "⬇️ ε-NFA'yı İndir",
                nfa_json,
                "epsilon_nfa.json",
                "application/json"
            )


# ==================== DFA COMPARISON ====================
elif menu_option == "4️⃣ DFA Karşılaştırma":
    st.header("⚖️ DFA Karşılaştırma")
    
    st.markdown("""
    İki DFA'nın **eşdeğerliğini** kontrol eder.
    Eşdeğerlik: L(DFA1) = L(DFA2) ?
    
    **Yöntem:** Symmetric Difference - L(A) △ L(B) = ∅ kontrolü
    """)
    
    col1, col2 = st.columns(2)
    
    dfa1, dfa2 = None, None
    
    with col1:
        st.subheader("DFA 1")
        
        dfa1_example = """{
  "states": ["q0", "q1"],
  "alphabet": ["a", "b"],
  "transitions": {
    "q0": {"a": "q1", "b": "q0"},
    "q1": {"a": "q1", "b": "q0"}
  },
  "start_state": "q0",
  "accept_states": ["q1"]
}"""
        
        if st.button("Örnek 1 Yükle", key="ex1"):
            st.session_state['dfa1_json'] = dfa1_example
        
        dfa1_json = st.text_area(
            "DFA 1 JSON:",
            value=st.session_state.get('dfa1_json', dfa1_example),
            height=250,
            key="dfa1_input"
        )
        
        try:
            dfa1 = parse_dfa_input(dfa1_json)
            st.success("✅ DFA 1 yüklendi")
            show_dfa_graph(dfa1, "DFA 1")
        except Exception as e:
            st.error(f"❌ Hata: {e}")
    
    with col2:
        st.subheader("DFA 2")
        
        dfa2_example = """{
  "states": ["s0", "s1", "s2"],
  "alphabet": ["a", "b"],
  "transitions": {
    "s0": {"a": "s1", "b": "s0"},
    "s1": {"a": "s2", "b": "s0"},
    "s2": {"a": "s1", "b": "s0"}
  },
  "start_state": "s0",
  "accept_states": ["s1", "s2"]
}"""
        
        if st.button("Örnek 2 Yükle", key="ex2"):
            st.session_state['dfa2_json'] = dfa2_example
        
        dfa2_json = st.text_area(
            "DFA 2 JSON:",
            value=st.session_state.get('dfa2_json', dfa2_example),
            height=250,
            key="dfa2_input"
        )
        
        try:
            dfa2 = parse_dfa_input(dfa2_json)
            st.success("✅ DFA 2 yüklendi")
            show_dfa_graph(dfa2, "DFA 2")
        except Exception as e:
            st.error(f"❌ Hata: {e}")
    
    if dfa1 and dfa2:
        st.divider()
        
        if st.button("⚖️ Karşılaştır", type="primary"):
            comparator = DFAComparison(dfa1, dfa2)
            is_equivalent, steps = comparator.are_equivalent()
            
            # Adımları göster
            for step in steps:
                with st.expander(f"Adım {step['step']}: {step['type']}", expanded=(step['type'] == 'result')):
                    st.markdown(f"```\n{step['description']}\n```")
                    
                    if 'product_dfa' in step:
                        show_dfa_graph(step['product_dfa'], "Symmetric Difference DFA")
            
            # Sonuç
            st.divider()
            if is_equivalent:
                st.success("## ✅ DFA'lar EŞDEĞERDİR")
                st.balloons()
            else:
                st.error("## ❌ DFA'lar EŞDEĞER DEĞİLDİR")
                counterexample = steps[-1].get('counterexample', '')
                st.warning(f"**Karşı örnek:** `{counterexample}`")
            
            # Detaylı karşılaştırma
            comparison = comparator.compare_languages()
            
            st.subheader("📊 Detaylı Karşılaştırma")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("L(DFA1) ⊆ L(DFA2)", "✓" if comparison['l1_subset_l2'] else "✗")
            with col2:
                st.metric("L(DFA2) ⊆ L(DFA1)", "✓" if comparison['l2_subset_l1'] else "✗")
            with col3:
                st.metric("İlişki", comparison['relationship'])
            
            # String test
            st.subheader("🧪 String Testi")
            test_strings = st.text_input("Test stringleri (virgülle ayırın):", "a, ab, abb, b, bb")
            
            if st.button("Stringleri Test Et"):
                strings = [s.strip() for s in test_strings.split(',')]
                results = comparator.test_strings(strings)
                
                for r in results:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**`{r['string']}`**")
                    with col2:
                        if r['dfa1_accepts']:
                            st.success("DFA1: ✓")
                        else:
                            st.error("DFA1: ✗")
                    with col3:
                        if r['dfa2_accepts']:
                            st.success("DFA2: ✓")
                        else:
                            st.error("DFA2: ✗")


# Footer
st.sidebar.divider()
st.sidebar.markdown("""
---
### 📖 Hakkında
**Finite Automata Toolkit**  
BIL 334 - Otomata Teorisi

Geliştirici: Adil
""")
