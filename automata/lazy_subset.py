"""
Lazy Subset Construction Algoritması
NFA'dan DFA'ya dönüşüm (on-demand / lazy yaklaşımı)
"""
from typing import Set, Dict, List, Tuple, Optional, Generator
from .nfa import NFA
from .dfa import DFA


class LazySubsetConstruction:
    """
    Lazy Subset Construction algoritması
    
    Normal subset construction tüm durumları önceden hesaplar.
    Lazy yaklaşımı sadece gereken durumları hesaplar (on-demand).
    """
    
    def __init__(self, nfa: NFA):
        """
        Args:
            nfa: Dönüştürülecek NFA
        """
        self.nfa = nfa
        self.dfa_states: Set[str] = set()
        self.dfa_transitions: Dict[str, Dict[str, str]] = {}
        self.dfa_accept_states: Set[str] = set()
        self.state_mapping: Dict[str, Set[str]] = {}  # DFA state -> NFA states
        self.reverse_mapping: Dict[frozenset, str] = {}  # NFA states -> DFA state
        self.state_counter = 0
        self.steps: List[dict] = []  # Adım adım kayıt
        
        # Başlangıç durumunu hesapla
        self._initialize()
    
    def _initialize(self):
        """Başlangıç durumunu oluştur"""
        # Başlangıç durumunun epsilon kapanışı
        start_nfa_states = self.nfa.epsilon_closure({self.nfa.start_state})
        self.dfa_start_state = self._get_or_create_state(start_nfa_states)
        
        self.steps.append({
            'type': 'init',
            'description': f"Başlangıç durumu: ε-closure({{{self.nfa.start_state}}}) = {{{', '.join(sorted(start_nfa_states))}}}",
            'nfa_states': start_nfa_states,
            'dfa_state': self.dfa_start_state,
            'current_dfa_states': set(self.dfa_states),
            'current_dfa_transitions': dict(self.dfa_transitions),
            'current_dfa_accept': set(self.dfa_accept_states)
        })
    
    def _get_or_create_state(self, nfa_states: Set[str]) -> str:
        """
        NFA durumları kümesi için DFA durumu al veya oluştur
        
        Args:
            nfa_states: NFA durumları kümesi
            
        Returns:
            DFA durum adı
        """
        frozen = frozenset(nfa_states)
        
        if frozen in self.reverse_mapping:
            return self.reverse_mapping[frozen]
        
        # Yeni durum oluştur
        state_name = f"q{self.state_counter}"
        self.state_counter += 1
        
        self.dfa_states.add(state_name)
        self.state_mapping[state_name] = nfa_states
        self.reverse_mapping[frozen] = state_name
        self.dfa_transitions[state_name] = {}
        
        # Kabul durumu mu kontrol et
        if nfa_states & self.nfa.accept_states:
            self.dfa_accept_states.add(state_name)
        
        return state_name
    
    def _compute_transition(self, dfa_state: str, symbol: str) -> Optional[str]:
        """
        Lazy olarak bir geçişi hesapla
        
        Args:
            dfa_state: DFA durumu
            symbol: Giriş sembolü
            
        Returns:
            Hedef DFA durumu veya None (boş küme için)
        """
        nfa_states = self.state_mapping[dfa_state]
        
        # NFA'da geçiş yap
        target_nfa_states = self.nfa.extended_transition(nfa_states, symbol)
        
        if not target_nfa_states:
            return None
        
        # DFA durumu al veya oluştur
        target_dfa_state = self._get_or_create_state(target_nfa_states)
        self.dfa_transitions[dfa_state][symbol] = target_dfa_state
        
        return target_dfa_state
    
    def convert_full(self) -> Generator[dict, None, DFA]:
        """
        Tam dönüşüm yap ve her adımı yield et
        
        Yields:
            Her adımın bilgisi
            
        Returns:
            Oluşturulan DFA
        """
        # Başlangıç adımını yield et
        yield self.steps[0]
        
        # İşlenecek durumlar (worklist algoritması)
        worklist = [self.dfa_start_state]
        processed = set()
        step_num = 1
        
        while worklist:
            current_state = worklist.pop(0)
            
            if current_state in processed:
                continue
            
            processed.add(current_state)
            nfa_states = self.state_mapping[current_state]
            
            # Her sembol için geçiş hesapla
            for symbol in sorted(self.nfa.alphabet):
                target_nfa_states = self.nfa.extended_transition(nfa_states, symbol)
                
                if not target_nfa_states:
                    step_info = {
                        'type': 'transition',
                        'step': step_num,
                        'from_state': current_state,
                        'from_nfa_states': nfa_states,
                        'symbol': symbol,
                        'to_nfa_states': set(),
                        'to_state': None,
                        'description': f"δ({current_state}, {symbol}) = δ({{{', '.join(sorted(nfa_states))}}}, {symbol}) = ∅",
                        'is_new_state': False,
                        'current_dfa_states': set(self.dfa_states),
                        'current_dfa_transitions': {s: dict(t) for s, t in self.dfa_transitions.items()},
                        'current_dfa_accept': set(self.dfa_accept_states)
                    }
                    self.steps.append(step_info)
                    yield step_info
                    step_num += 1
                    continue
                
                # Yeni durum mu kontrol et
                frozen = frozenset(target_nfa_states)
                is_new = frozen not in self.reverse_mapping
                
                target_state = self._get_or_create_state(target_nfa_states)
                self.dfa_transitions[current_state][symbol] = target_state
                
                if is_new:
                    worklist.append(target_state)
                
                # Move ve epsilon closure açıklaması
                move_states = self.nfa.move(nfa_states, symbol)
                
                step_info = {
                    'type': 'transition',
                    'step': step_num,
                    'from_state': current_state,
                    'from_nfa_states': nfa_states,
                    'symbol': symbol,
                    'move_result': move_states,
                    'to_nfa_states': target_nfa_states,
                    'to_state': target_state,
                    'description': (
                        f"δ({current_state}, {symbol}):\n"
                        f"  move({{{', '.join(sorted(nfa_states))}}}, {symbol}) = {{{', '.join(sorted(move_states))}}}\n"
                        f"  ε-closure({{{', '.join(sorted(move_states))}}}) = {{{', '.join(sorted(target_nfa_states))}}}\n"
                        f"  → {target_state}" + (" (YENİ DURUM)" if is_new else " (mevcut)")
                    ),
                    'is_new_state': is_new,
                    'current_dfa_states': set(self.dfa_states),
                    'current_dfa_transitions': {s: dict(t) for s, t in self.dfa_transitions.items()},
                    'current_dfa_accept': set(self.dfa_accept_states)
                }
                self.steps.append(step_info)
                yield step_info
                step_num += 1
        
        # Son DFA'yı oluştur
        return self.get_dfa()
    
    def convert(self) -> DFA:
        """
        NFA'yı DFA'ya dönüştür (adım adım takip etmeden)
        
        Returns:
            Oluşturulan DFA
        """
        # Generator'ı tüket
        for _ in self.convert_full():
            pass
        
        return self.get_dfa()
    
    def get_dfa(self) -> DFA:
        """Mevcut DFA'yı döndür"""
        return DFA(
            states=self.dfa_states.copy(),
            alphabet=self.nfa.alphabet.copy(),
            transitions={s: dict(t) for s, t in self.dfa_transitions.items()},
            start_state=self.dfa_start_state,
            accept_states=self.dfa_accept_states.copy(),
            state_mapping={s: set(nfa_s) for s, nfa_s in self.state_mapping.items()}
        )
    
    def get_state_label(self, dfa_state: str) -> str:
        """DFA durumu için NFA durumlarını gösteren etiket"""
        nfa_states = self.state_mapping.get(dfa_state, set())
        return '{' + ', '.join(sorted(nfa_states)) + '}'
    
    def get_all_steps(self) -> List[dict]:
        """Tüm adımları döndür"""
        return self.steps


def subset_construction(nfa: NFA) -> Tuple[DFA, List[dict]]:
    """
    Convenience function: NFA'dan DFA'ya dönüştür
    
    Args:
        nfa: Dönüştürülecek NFA
        
    Returns:
        (DFA, adımlar listesi)
    """
    converter = LazySubsetConstruction(nfa)
    dfa = converter.convert()
    return dfa, converter.get_all_steps()
