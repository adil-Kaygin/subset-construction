"""
DFA Comparison (Eşdeğerlik Kontrolü)
İki DFA'nın aynı dili kabul edip etmediğini kontrol eder
"""
from typing import Set, Dict, List, Tuple, Optional
from .dfa import DFA
from .minimization import DFAMinimization


class DFAComparison:
    """
    İki DFA'nın eşdeğerliğini kontrol eden sınıf
    
    Yöntemler:
    1. Product Construction - İki DFA'nın çarpım otomatı
    2. Symmetric Difference - L(A) △ L(B) = ∅ kontrolü
    3. Minimization Comparison - Minimize edip karşılaştırma
    """
    
    def __init__(self, dfa1: DFA, dfa2: DFA):
        """
        Args:
            dfa1: İlk DFA
            dfa2: İkinci DFA
        """
        self.dfa1 = dfa1
        self.dfa2 = dfa2
        self.steps: List[dict] = []
        
        # Alfabelerin uyumlu olduğunu kontrol et
        if dfa1.alphabet != dfa2.alphabet:
            # Birleştir
            self.alphabet = dfa1.alphabet | dfa2.alphabet
        else:
            self.alphabet = dfa1.alphabet
    
    def _product_construction(
        self, 
        accept_condition: str = 'symmetric_difference'
    ) -> DFA:
        """
        İki DFA'nın çarpım otomatını oluştur
        
        Args:
            accept_condition: 
                'intersection' - her iki DFA da kabul ederse
                'union' - en az biri kabul ederse
                'symmetric_difference' - sadece biri kabul ederse
                'difference_1_2' - DFA1 kabul, DFA2 red
                'difference_2_1' - DFA2 kabul, DFA1 red
        
        Returns:
            Çarpım DFA
        """
        # DFA'ları tamamla
        dfa1 = self.dfa1.make_complete("dead1")
        dfa2 = self.dfa2.make_complete("dead2")
        
        # Çarpım durumları
        product_states = set()
        product_transitions = {}
        product_accept = set()
        
        # BFS ile erişilebilir durumları bul
        start = (dfa1.start_state, dfa2.start_state)
        start_name = f"({start[0]},{start[1]})"
        
        visited = set()
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            s1, s2 = current
            state_name = f"({s1},{s2})"
            product_states.add(state_name)
            product_transitions[state_name] = {}
            
            # Kabul durumu mu?
            in_accept1 = s1 in dfa1.accept_states
            in_accept2 = s2 in dfa2.accept_states
            
            is_accept = False
            if accept_condition == 'intersection':
                is_accept = in_accept1 and in_accept2
            elif accept_condition == 'union':
                is_accept = in_accept1 or in_accept2
            elif accept_condition == 'symmetric_difference':
                is_accept = in_accept1 != in_accept2
            elif accept_condition == 'difference_1_2':
                is_accept = in_accept1 and not in_accept2
            elif accept_condition == 'difference_2_1':
                is_accept = in_accept2 and not in_accept1
            
            if is_accept:
                product_accept.add(state_name)
            
            # Geçişler
            for symbol in self.alphabet:
                next1 = dfa1.transition(s1, symbol) or "dead1"
                next2 = dfa2.transition(s2, symbol) or "dead2"
                
                next_state = (next1, next2)
                next_name = f"({next1},{next2})"
                
                product_transitions[state_name][symbol] = next_name
                
                if next_state not in visited:
                    queue.append(next_state)
        
        return DFA(
            states=product_states,
            alphabet=self.alphabet,
            transitions=product_transitions,
            start_state=start_name,
            accept_states=product_accept
        )
    
    def are_equivalent(self) -> Tuple[bool, List[dict]]:
        """
        İki DFA'nın eşdeğer olup olmadığını kontrol et
        
        Returns:
            (eşdeğer mi?, adımlar)
        """
        self.steps = []
        
        # Adım 1: Symmetric difference DFA oluştur
        self.steps.append({
            'type': 'start',
            'step': 1,
            'description': "İki DFA'nın eşdeğerliği kontrol ediliyor...\n"
                          f"DFA1: {len(self.dfa1.states)} durum\n"
                          f"DFA2: {len(self.dfa2.states)} durum\n"
                          "Yöntem: Symmetric Difference L(A) △ L(B) = ∅ ?"
        })
        
        # Adım 2: Product construction
        sym_diff_dfa = self._product_construction('symmetric_difference')
        
        self.steps.append({
            'type': 'product',
            'step': 2,
            'description': f"Symmetric difference DFA oluşturuldu.\n"
                          f"Çarpım durumları: {len(sym_diff_dfa.states)}\n"
                          f"Kabul durumları: {sym_diff_dfa.accept_states}",
            'product_dfa': sym_diff_dfa
        })
        
        # Adım 3: Kabul durumuna erişilebilir mi kontrol et
        reachable = sym_diff_dfa.get_reachable_states()
        reachable_accept = reachable & sym_diff_dfa.accept_states
        
        is_equivalent = len(reachable_accept) == 0
        
        if is_equivalent:
            self.steps.append({
                'type': 'result',
                'step': 3,
                'description': "✅ DFA'lar EŞDEĞERDİR!\n"
                              "Symmetric difference otomatının kabul durumuna ulaşılamıyor.\n"
                              "L(DFA1) = L(DFA2)",
                'is_equivalent': True,
                'counterexample': None
            })
        else:
            # Karşı örnek bul
            counterexample = self._find_counterexample(sym_diff_dfa)
            
            self.steps.append({
                'type': 'result',
                'step': 3,
                'description': f"❌ DFA'lar EŞDEĞER DEĞİLDİR!\n"
                              f"Karşı örnek: '{counterexample}'\n"
                              f"Bu string bir DFA tarafından kabul edilir, diğeri tarafından reddedilir.",
                'is_equivalent': False,
                'counterexample': counterexample
            })
        
        return is_equivalent, self.steps
    
    def _find_counterexample(self, sym_diff_dfa: DFA) -> str:
        """BFS ile karşı örnek bul"""
        queue = [(sym_diff_dfa.start_state, "")]
        visited = {sym_diff_dfa.start_state}
        
        while queue:
            state, path = queue.pop(0)
            
            # Kabul durumuna ulaştık mı?
            if state in sym_diff_dfa.accept_states:
                return path if path else "ε"
            
            # Komşuları ekle
            if state in sym_diff_dfa.transitions:
                for symbol, next_state in sym_diff_dfa.transitions[state].items():
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append((next_state, path + symbol))
        
        return ""
    
    def get_intersection(self) -> DFA:
        """İki DFA'nın kesişimini döndür (L1 ∩ L2)"""
        return self._product_construction('intersection')
    
    def get_union(self) -> DFA:
        """İki DFA'nın birleşimini döndür (L1 ∪ L2)"""
        return self._product_construction('union')
    
    def get_difference(self, which: int = 1) -> DFA:
        """
        Fark DFA'sı (L1 - L2 veya L2 - L1)
        
        Args:
            which: 1 için L1-L2, 2 için L2-L1
        """
        if which == 1:
            return self._product_construction('difference_1_2')
        else:
            return self._product_construction('difference_2_1')
    
    def compare_languages(self) -> dict:
        """
        İki DFA'nın dillerini kapsamlı karşılaştır
        
        Returns:
            Karşılaştırma sonuçları
        """
        is_equivalent, _ = self.are_equivalent()
        
        # L1 ⊆ L2 kontrolü
        diff_1_2 = self._product_construction('difference_1_2')
        reachable_1_2 = diff_1_2.get_reachable_states() & diff_1_2.accept_states
        l1_subset_l2 = len(reachable_1_2) == 0
        
        # L2 ⊆ L1 kontrolü
        diff_2_1 = self._product_construction('difference_2_1')
        reachable_2_1 = diff_2_1.get_reachable_states() & diff_2_1.accept_states
        l2_subset_l1 = len(reachable_2_1) == 0
        
        return {
            'equivalent': is_equivalent,
            'l1_subset_l2': l1_subset_l2,
            'l2_subset_l1': l2_subset_l1,
            'relationship': self._determine_relationship(is_equivalent, l1_subset_l2, l2_subset_l1)
        }
    
    def _determine_relationship(
        self, 
        equivalent: bool, 
        l1_subset_l2: bool, 
        l2_subset_l1: bool
    ) -> str:
        """Diller arasındaki ilişkiyi belirle"""
        if equivalent:
            return "L(DFA1) = L(DFA2)"
        elif l1_subset_l2 and not l2_subset_l1:
            return "L(DFA1) ⊂ L(DFA2)"
        elif l2_subset_l1 and not l1_subset_l2:
            return "L(DFA2) ⊂ L(DFA1)"
        else:
            return "L(DFA1) ve L(DFA2) kısmen örtüşüyor"
    
    def test_strings(self, strings: List[str]) -> List[dict]:
        """
        Verilen stringleri her iki DFA'da test et
        
        Args:
            strings: Test edilecek stringler
            
        Returns:
            Test sonuçları
        """
        results = []
        for s in strings:
            result1 = self.dfa1.accepts(s)
            result2 = self.dfa2.accepts(s)
            results.append({
                'string': s if s else 'ε',
                'dfa1_accepts': result1,
                'dfa2_accepts': result2,
                'same_result': result1 == result2
            })
        return results


def compare_dfas(dfa1: DFA, dfa2: DFA) -> Tuple[bool, str, List[dict]]:
    """
    Convenience function: İki DFA'yı karşılaştır
    
    Args:
        dfa1: İlk DFA
        dfa2: İkinci DFA
        
    Returns:
        (eşdeğer mi?, ilişki açıklaması, adımlar)
    """
    comparator = DFAComparison(dfa1, dfa2)
    is_equivalent, steps = comparator.are_equivalent()
    comparison = comparator.compare_languages()
    
    return is_equivalent, comparison['relationship'], steps
