"""
NFA (Non-deterministic Finite Automaton) veri yapısı
"""
import json
from typing import Set, Dict, List, FrozenSet, Optional


class NFA:
    """
    Non-deterministic Finite Automaton (NFA) sınıfı
    
    Attributes:
        states: Durumlar kümesi
        alphabet: Alfabe (giriş sembolleri)
        transitions: Geçiş fonksiyonu {state: {symbol: {states}}}
        start_state: Başlangıç durumu
        accept_states: Kabul durumları kümesi
    """
    
    EPSILON = 'ε'  # Epsilon sembolü
    
    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[str, Dict[str, Set[str]]],
        start_state: str,
        accept_states: Set[str]
    ):
        self.states = states
        self.alphabet = alphabet - {self.EPSILON}  # Epsilon alfabede değil
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self._validate()
    
    def _validate(self):
        """NFA'nın geçerli olup olmadığını kontrol et"""
        if self.start_state not in self.states:
            raise ValueError(f"Başlangıç durumu '{self.start_state}' durumlar kümesinde değil")
        
        if not self.accept_states.issubset(self.states):
            invalid = self.accept_states - self.states
            raise ValueError(f"Kabul durumları {invalid} durumlar kümesinde değil")
    
    def epsilon_closure(self, states: Set[str]) -> Set[str]:
        """
        Verilen durumların epsilon kapanışını hesapla
        
        Args:
            states: Başlangıç durumları kümesi
            
        Returns:
            Epsilon kapanışı (epsilon geçişleriyle ulaşılabilir tüm durumlar)
        """
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            if state in self.transitions:
                epsilon_targets = self.transitions[state].get(self.EPSILON, set())
                for target in epsilon_targets:
                    if target not in closure:
                        closure.add(target)
                        stack.append(target)
        
        return closure
    
    def move(self, states: Set[str], symbol: str) -> Set[str]:
        """
        Verilen durumlardan bir sembolle ulaşılabilir durumları bul
        
        Args:
            states: Mevcut durumlar kümesi
            symbol: Giriş sembolü
            
        Returns:
            Ulaşılabilir durumlar kümesi
        """
        result = set()
        for state in states:
            if state in self.transitions:
                targets = self.transitions[state].get(symbol, set())
                result.update(targets)
        return result
    
    def extended_transition(self, states: Set[str], symbol: str) -> Set[str]:
        """
        Epsilon kapanışı dahil genişletilmiş geçiş fonksiyonu
        
        Args:
            states: Mevcut durumlar kümesi
            symbol: Giriş sembolü
            
        Returns:
            Epsilon kapanışı dahil ulaşılabilir durumlar
        """
        # Önce move, sonra epsilon closure
        moved = self.move(states, symbol)
        return self.epsilon_closure(moved)
    
    def accepts(self, input_string: str) -> bool:
        """
        NFA'nın verilen stringi kabul edip etmediğini kontrol et
        
        Args:
            input_string: Kontrol edilecek string
            
        Returns:
            True eğer kabul ederse, False aksi halde
        """
        current_states = self.epsilon_closure({self.start_state})
        
        for symbol in input_string:
            current_states = self.extended_transition(current_states, symbol)
            if not current_states:
                return False
        
        return bool(current_states & self.accept_states)
    
    def has_epsilon_transitions(self) -> bool:
        """NFA'da epsilon geçişi olup olmadığını kontrol et"""
        for state, trans in self.transitions.items():
            if self.EPSILON in trans and trans[self.EPSILON]:
                return True
        return False
    
    @classmethod
    def from_json(cls, json_data: dict) -> 'NFA':
        """
        JSON verisinden NFA oluştur
        
        Args:
            json_data: NFA tanımını içeren dictionary
            
        Returns:
            NFA nesnesi
        """
        states = set(json_data['states'])
        alphabet = set(json_data['alphabet'])
        start_state = json_data['start_state']
        accept_states = set(json_data['accept_states'])
        
        # Transitions'ı dönüştür
        transitions = {}
        for state, trans in json_data['transitions'].items():
            transitions[state] = {}
            for symbol, targets in trans.items():
                if isinstance(targets, list):
                    transitions[state][symbol] = set(targets)
                else:
                    transitions[state][symbol] = {targets}
        
        return cls(states, alphabet, transitions, start_state, accept_states)
    
    @classmethod
    def from_json_file(cls, filepath: str) -> 'NFA':
        """JSON dosyasından NFA oluştur"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_json(data)
    
    def to_json(self) -> dict:
        """NFA'yı JSON formatına dönüştür"""
        transitions = {}
        for state, trans in self.transitions.items():
            transitions[state] = {}
            for symbol, targets in trans.items():
                transitions[state][symbol] = list(targets)
        
        return {
            'states': list(self.states),
            'alphabet': list(self.alphabet),
            'transitions': transitions,
            'start_state': self.start_state,
            'accept_states': list(self.accept_states)
        }
    
    def to_json_file(self, filepath: str):
        """NFA'yı JSON dosyasına kaydet"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_json(), f, indent=2, ensure_ascii=False)
    
    def __repr__(self):
        return f"NFA(states={self.states}, start={self.start_state}, accept={self.accept_states})"
