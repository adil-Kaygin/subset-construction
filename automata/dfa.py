"""
DFA (Deterministic Finite Automaton) veri yapısı
"""
import json
from typing import Set, Dict, List, Optional


class DFA:
    """
    Deterministic Finite Automaton (DFA) sınıfı
    
    Attributes:
        states: Durumlar kümesi
        alphabet: Alfabe (giriş sembolleri)
        transitions: Geçiş fonksiyonu {state: {symbol: state}}
        start_state: Başlangıç durumu
        accept_states: Kabul durumları kümesi
        state_mapping: NFA durumlarından DFA durumlarına eşleme (subset construction için)
    """
    
    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[str, Dict[str, str]],
        start_state: str,
        accept_states: Set[str],
        state_mapping: Optional[Dict[str, Set[str]]] = None
    ):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.state_mapping = state_mapping or {}
        self._validate()
    
    def _validate(self):
        """DFA'nın geçerli olup olmadığını kontrol et"""
        if self.start_state not in self.states:
            raise ValueError(f"Başlangıç durumu '{self.start_state}' durumlar kümesinde değil")
        
        if not self.accept_states.issubset(self.states):
            invalid = self.accept_states - self.states
            raise ValueError(f"Kabul durumları {invalid} durumlar kümesinde değil")
    
    def transition(self, state: str, symbol: str) -> Optional[str]:
        """
        Geçiş fonksiyonu
        
        Args:
            state: Mevcut durum
            symbol: Giriş sembolü
            
        Returns:
            Hedef durum veya None
        """
        if state in self.transitions:
            return self.transitions[state].get(symbol)
        return None
    
    def accepts(self, input_string: str) -> bool:
        """
        DFA'nın verilen stringi kabul edip etmediğini kontrol et
        
        Args:
            input_string: Kontrol edilecek string
            
        Returns:
            True eğer kabul ederse, False aksi halde
        """
        current_state = self.start_state
        
        for symbol in input_string:
            next_state = self.transition(current_state, symbol)
            if next_state is None:
                return False
            current_state = next_state
        
        return current_state in self.accept_states
    
    def is_complete(self) -> bool:
        """DFA'nın tam olup olmadığını kontrol et (her durumda her sembol için geçiş var mı)"""
        for state in self.states:
            for symbol in self.alphabet:
                if self.transition(state, symbol) is None:
                    return False
        return True
    
    def make_complete(self, dead_state: str = "dead") -> 'DFA':
        """
        DFA'yı tamamla (eksik geçişler için dead state ekle)
        
        Args:
            dead_state: Ölü durum adı
            
        Returns:
            Tamamlanmış DFA
        """
        if self.is_complete():
            return self
        
        new_states = self.states.copy()
        new_transitions = {s: dict(t) for s, t in self.transitions.items()}
        needs_dead_state = False
        
        # Eksik geçişleri bul ve dead state'e yönlendir
        for state in self.states:
            if state not in new_transitions:
                new_transitions[state] = {}
            for symbol in self.alphabet:
                if symbol not in new_transitions[state]:
                    new_transitions[state][symbol] = dead_state
                    needs_dead_state = True
        
        # Dead state'i ekle
        if needs_dead_state:
            new_states.add(dead_state)
            new_transitions[dead_state] = {symbol: dead_state for symbol in self.alphabet}
        
        return DFA(
            new_states,
            self.alphabet.copy(),
            new_transitions,
            self.start_state,
            self.accept_states.copy(),
            self.state_mapping.copy()
        )
    
    def get_reachable_states(self) -> Set[str]:
        """Başlangıç durumundan ulaşılabilir durumları bul"""
        reachable = {self.start_state}
        stack = [self.start_state]
        
        while stack:
            state = stack.pop()
            if state in self.transitions:
                for symbol, target in self.transitions[state].items():
                    if target not in reachable:
                        reachable.add(target)
                        stack.append(target)
        
        return reachable
    
    def remove_unreachable_states(self) -> 'DFA':
        """Ulaşılamaz durumları kaldır"""
        reachable = self.get_reachable_states()
        
        new_states = self.states & reachable
        new_accept = self.accept_states & reachable
        new_transitions = {}
        
        for state in reachable:
            if state in self.transitions:
                new_transitions[state] = {
                    s: t for s, t in self.transitions[state].items() 
                    if t in reachable
                }
        
        new_mapping = {k: v for k, v in self.state_mapping.items() if k in reachable}
        
        return DFA(
            new_states,
            self.alphabet.copy(),
            new_transitions,
            self.start_state,
            new_accept,
            new_mapping
        )
    
    @classmethod
    def from_json(cls, json_data: dict) -> 'DFA':
        """JSON verisinden DFA oluştur"""
        states = set(json_data['states'])
        alphabet = set(json_data['alphabet'])
        start_state = json_data['start_state']
        accept_states = set(json_data['accept_states'])
        
        transitions = {}
        for state, trans in json_data['transitions'].items():
            transitions[state] = dict(trans)
        
        state_mapping = {}
        if 'state_mapping' in json_data:
            for state, nfa_states in json_data['state_mapping'].items():
                state_mapping[state] = set(nfa_states)
        
        return cls(states, alphabet, transitions, start_state, accept_states, state_mapping)
    
    @classmethod
    def from_json_file(cls, filepath: str) -> 'DFA':
        """JSON dosyasından DFA oluştur"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_json(data)
    
    def to_json(self) -> dict:
        """DFA'yı JSON formatına dönüştür"""
        result = {
            'states': list(self.states),
            'alphabet': list(self.alphabet),
            'transitions': self.transitions,
            'start_state': self.start_state,
            'accept_states': list(self.accept_states)
        }
        
        if self.state_mapping:
            result['state_mapping'] = {k: list(v) for k, v in self.state_mapping.items()}
        
        return result
    
    def to_json_file(self, filepath: str):
        """DFA'yı JSON dosyasına kaydet"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_json(), f, indent=2, ensure_ascii=False)
    
    def __repr__(self):
        return f"DFA(states={self.states}, start={self.start_state}, accept={self.accept_states})"
