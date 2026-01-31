"""
Automata Görselleştirme Modülü
Graphviz kullanarak NFA ve DFA görselleştirmesi
"""
import graphviz
from typing import Set, Dict, Optional, List
import os


class AutomataVisualizer:
    """NFA ve DFA görselleştirme sınıfı"""
    
    def __init__(self, output_dir: str = "output"):
        """
        Args:
            output_dir: Çıktı dosyalarının kaydedileceği dizin
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def visualize_nfa(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[str, Dict[str, Set[str]]],
        start_state: str,
        accept_states: Set[str],
        title: str = "NFA",
        highlight_states: Optional[Set[str]] = None,
        highlight_edges: Optional[List[tuple]] = None,
        filename: Optional[str] = None
    ) -> graphviz.Digraph:
        """
        NFA'yı görselleştir
        
        Args:
            states: Durumlar kümesi
            alphabet: Alfabe
            transitions: Geçiş fonksiyonu
            start_state: Başlangıç durumu
            accept_states: Kabul durumları
            title: Grafik başlığı
            highlight_states: Vurgulanacak durumlar
            highlight_edges: Vurgulanacak kenarlar [(from, to, symbol), ...]
            filename: Çıktı dosya adı (None ise kaydetmez)
            
        Returns:
            Graphviz Digraph nesnesi
        """
        dot = graphviz.Digraph(comment=title)
        dot.attr(rankdir='LR', label=title, labelloc='t', fontsize='16')
        
        highlight_states = highlight_states or set()
        highlight_edges = highlight_edges or []
        highlight_edge_set = {(e[0], e[1], e[2]) for e in highlight_edges}
        
        # Görünmez başlangıç düğümü
        dot.node('__start__', '', shape='none', width='0', height='0')
        
        # Durumları ekle
        for state in states:
            if state in accept_states:
                shape = 'doublecircle'
            else:
                shape = 'circle'
            
            # Vurgulama rengi
            if state in highlight_states:
                dot.node(state, state, shape=shape, style='filled', fillcolor='lightblue')
            else:
                dot.node(state, state, shape=shape)
        
        # Başlangıç oku
        dot.edge('__start__', start_state)
        
        # Geçişleri ekle (aynı durumlar arasındaki geçişleri birleştir)
        edge_labels = {}  # (from, to) -> [labels]
        
        for state, trans in transitions.items():
            for symbol, targets in trans.items():
                for target in targets:
                    key = (state, target)
                    if key not in edge_labels:
                        edge_labels[key] = []
                    edge_labels[key].append(symbol)
        
        for (from_state, to_state), labels in edge_labels.items():
            label = ', '.join(sorted(labels))
            
            # Vurgulanacak kenar mı kontrol et
            is_highlighted = any(
                (from_state, to_state, lbl) in highlight_edge_set 
                for lbl in labels
            )
            
            if is_highlighted:
                dot.edge(from_state, to_state, label=label, color='red', penwidth='2')
            else:
                dot.edge(from_state, to_state, label=label)
        
        # Dosyaya kaydet
        if filename:
            filepath = os.path.join(self.output_dir, filename)
            dot.render(filepath, format='png', cleanup=True)
        
        return dot
    
    def visualize_dfa(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[str, Dict[str, str]],
        start_state: str,
        accept_states: Set[str],
        title: str = "DFA",
        state_labels: Optional[Dict[str, str]] = None,
        highlight_states: Optional[Set[str]] = None,
        highlight_edges: Optional[List[tuple]] = None,
        filename: Optional[str] = None
    ) -> graphviz.Digraph:
        """
        DFA'yı görselleştir
        
        Args:
            states: Durumlar kümesi
            alphabet: Alfabe
            transitions: Geçiş fonksiyonu
            start_state: Başlangıç durumu
            accept_states: Kabul durumları
            title: Grafik başlığı
            state_labels: Durum etiketleri (alt satırda gösterilir)
            highlight_states: Vurgulanacak durumlar
            highlight_edges: Vurgulanacak kenarlar
            filename: Çıktı dosya adı
            
        Returns:
            Graphviz Digraph nesnesi
        """
        dot = graphviz.Digraph(comment=title)
        dot.attr(rankdir='LR', label=title, labelloc='t', fontsize='16')
        
        highlight_states = highlight_states or set()
        highlight_edges = highlight_edges or []
        highlight_edge_set = {(e[0], e[1], e[2]) for e in highlight_edges}
        state_labels = state_labels or {}
        
        # Görünmez başlangıç düğümü
        dot.node('__start__', '', shape='none', width='0', height='0')
        
        # Durumları ekle
        for state in states:
            if state in accept_states:
                shape = 'doublecircle'
            else:
                shape = 'circle'
            
            # Etiket oluştur
            if state in state_labels:
                label = f"{state}\n{state_labels[state]}"
            else:
                label = state
            
            # Vurgulama rengi
            if state in highlight_states:
                dot.node(state, label, shape=shape, style='filled', fillcolor='lightgreen')
            else:
                dot.node(state, label, shape=shape)
        
        # Başlangıç oku
        dot.edge('__start__', start_state)
        
        # Geçişleri ekle
        edge_labels = {}
        
        for state, trans in transitions.items():
            for symbol, target in trans.items():
                key = (state, target)
                if key not in edge_labels:
                    edge_labels[key] = []
                edge_labels[key].append(symbol)
        
        for (from_state, to_state), labels in edge_labels.items():
            label = ', '.join(sorted(labels))
            
            is_highlighted = any(
                (from_state, to_state, lbl) in highlight_edge_set 
                for lbl in labels
            )
            
            if is_highlighted:
                dot.edge(from_state, to_state, label=label, color='red', penwidth='2')
            else:
                dot.edge(from_state, to_state, label=label)
        
        if filename:
            filepath = os.path.join(self.output_dir, filename)
            dot.render(filepath, format='png', cleanup=True)
        
        return dot
    
    def visualize_subset_construction_step(
        self,
        nfa_states: Set[str],
        nfa_alphabet: Set[str],
        nfa_transitions: Dict[str, Dict[str, Set[str]]],
        nfa_start: str,
        nfa_accept: Set[str],
        dfa_states: Set[str],
        dfa_transitions: Dict[str, Dict[str, str]],
        dfa_start: str,
        dfa_accept: Set[str],
        state_mapping: Dict[str, Set[str]],
        current_state: str,
        current_symbol: Optional[str],
        new_state: Optional[str],
        step_number: int
    ) -> tuple:
        """
        Subset construction adımını görselleştir
        
        Returns:
            (nfa_graph, dfa_graph) tuple
        """
        # NFA'yı görselleştir (mevcut durumları vurgula)
        current_nfa_states = state_mapping.get(current_state, set())
        nfa_graph = self.visualize_nfa(
            nfa_states, nfa_alphabet, nfa_transitions, nfa_start, nfa_accept,
            title=f"NFA - Adım {step_number}",
            highlight_states=current_nfa_states
        )
        
        # DFA'yı görselleştir
        highlight_edges = []
        if current_symbol and new_state:
            highlight_edges = [(current_state, new_state, current_symbol)]
        
        # Durum etiketleri oluştur
        state_labels = {}
        for dfa_state, nfa_set in state_mapping.items():
            state_labels[dfa_state] = '{' + ','.join(sorted(nfa_set)) + '}'
        
        dfa_graph = self.visualize_dfa(
            dfa_states, nfa_alphabet, dfa_transitions, dfa_start, dfa_accept,
            title=f"DFA - Adım {step_number}",
            state_labels=state_labels,
            highlight_states={current_state} if current_state else set(),
            highlight_edges=highlight_edges
        )
        
        return nfa_graph, dfa_graph
    
    def visualize_minimization_step(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[str, Dict[str, str]],
        start_state: str,
        accept_states: Set[str],
        partition: List[Set[str]],
        step_number: int,
        title: str = "DFA Minimization"
    ) -> graphviz.Digraph:
        """
        DFA minimization adımını görselleştir
        Aynı partition'daki durumlar aynı renkle gösterilir
        """
        dot = graphviz.Digraph(comment=title)
        dot.attr(rankdir='LR', label=f"{title} - Adım {step_number}", labelloc='t', fontsize='16')
        
        # Renkler
        colors = [
            'lightblue', 'lightgreen', 'lightyellow', 'lightpink', 
            'lightcoral', 'lightsalmon', 'lightgray', 'lavender',
            'palegreen', 'peachpuff', 'plum', 'powderblue'
        ]
        
        # Durum -> renk eşlemesi
        state_colors = {}
        for i, group in enumerate(partition):
            color = colors[i % len(colors)]
            for state in group:
                state_colors[state] = color
        
        # Görünmez başlangıç düğümü
        dot.node('__start__', '', shape='none', width='0', height='0')
        
        # Durumları ekle
        for state in states:
            shape = 'doublecircle' if state in accept_states else 'circle'
            color = state_colors.get(state, 'white')
            dot.node(state, state, shape=shape, style='filled', fillcolor=color)
        
        # Başlangıç oku
        dot.edge('__start__', start_state)
        
        # Geçişleri ekle
        edge_labels = {}
        for state, trans in transitions.items():
            for symbol, target in trans.items():
                key = (state, target)
                if key not in edge_labels:
                    edge_labels[key] = []
                edge_labels[key].append(symbol)
        
        for (from_state, to_state), labels in edge_labels.items():
            label = ', '.join(sorted(labels))
            dot.edge(from_state, to_state, label=label)
        
        # Partition bilgisini alt kısımda göster
        partition_info = " | ".join(['{' + ','.join(sorted(g)) + '}' for g in partition])
        dot.attr(label=f"{title} - Adım {step_number}\nPartition: {partition_info}")
        
        return dot
    
    def visualize_regex_construction_step(
        self,
        nfa_states: Set[str],
        nfa_transitions: Dict[str, Dict[str, Set[str]]],
        nfa_start: str,
        nfa_accept: Set[str],
        step_description: str,
        step_number: int
    ) -> graphviz.Digraph:
        """
        Regex to NFA construction adımını görselleştir
        """
        return self.visualize_nfa(
            nfa_states, set(), nfa_transitions, nfa_start, nfa_accept,
            title=f"Regex → ε-NFA - Adım {step_number}\n{step_description}"
        )
