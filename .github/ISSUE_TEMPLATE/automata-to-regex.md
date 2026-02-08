---
name: NFA/DFA → RE Dönüşümü
about: Finite Automata'dan Regular Expression elde etme özelliği
title: '[FEATURE] NFA/DFA → RE Dönüşümü (State Elimination Algoritması)'
labels: ['enhancement', 'good first issue', 'help wanted']
assignees: ''
---

## 🎯 Özellik Açıklaması

Kullanıcıların bir NFA veya DFA vererek, bu otomatın kabul ettiği dili temsil eden Regular Expression (RE) elde edebilmelerini sağlayan bir modül ve UI eklenmesi.

## 📋 Detaylı Gereksinimler

### Dönüşüm Yöntemi

**State Elimination (Durum Eliminasyonu)** algoritması kullanılarak NFA/DFA → RE dönüşümü yapılacak.

### Algoritma Adımları

1. **Ön İşleme**
   - Tek bir başlangıç durumu olduğundan emin ol (yoksa yeni başlangıç durumu ekle)
   - Tek bir kabul durumu olduğundan emin ol (yoksa yeni kabul durumu ekle)
   - Başlangıç durumundan gelen ve kabul durumuna giden epsilon geçişler ekle

2. **Durum Eliminasyonu**
   - Başlangıç ve kabul dışındaki her durumu sırayla ele al
   - Eliminasyon sırasında regex ifadeleri oluştur
   - Her eliminasyonda geçiş etiketlerini regex olarak güncelle

3. **Son Regex Oluşturma**
   - Sadece başlangıç ve kabul durumu kalana kadar devam et
   - Aralarındaki regex son Regular Expression'dır

### State Elimination Formülü

Bir `q` durumu elimine edilirken, `qi` den `qj` ye giden yeni regex:

```
R_new(qi, qj) = R(qi, qj) | R(qi, q) · R(q, q)* · R(q, qj)
```

Burada:
- `R(qi, qj)`: qi'den qj'ye direkt geçiş regex'i
- `R(qi, q)`: qi'den q'ya geçiş regex'i  
- `R(q, q)`: q'dan kendisine geçiş regex'i
- `R(q, qj)`: q'dan qj'ye geçiş regex'i
- `|`: union (veya)
- `·`: concatenation
- `*`: Kleene star

## 🔧 Teknik Detaylar

### Yeni Eklenecek Dosya

`automata/automata_to_regex.py` dosyası oluşturulacak:

```python
class AutomataToRegex:
    """
    State Elimination algoritması ile NFA/DFA → RE dönüşümü
    """
    
    def __init__(self, automata):
        """
        Args:
            automata: NFA veya DFA objesi
        """
        self.automata = automata
        self.steps = []  # Görselleştirme için adımlar
    
    def convert(self) -> str:
        """
        Otomatı regex'e dönüştür
        
        Returns:
            Regular expression string
        """
        # Algoritma implementasyonu
        pass
    
    def _preprocess(self):
        """Tek başlangıç ve tek kabul durumu ekle"""
        pass
    
    def _eliminate_state(self, state):
        """Bir durumu elimine et ve regex'leri güncelle"""
        pass
    
    def _choose_elimination_order(self) -> List[str]:
        """Durum eliminasyon sırasını belirle"""
        pass
```

### UI Gereksinimleri

`app.py` içine yeni menü seçeneği:

```python
"5️⃣ NFA/DFA → RE"  # veya "6️⃣" RE Karşılaştırma eklenirse
```

### UI Bileşenleri

1. **Giriş**
   - Automata tipi seçimi (NFA / DFA)
   - JSON input (textarea veya file upload)
   - Örnek otomatlar için dropdown

2. **Görselleştirme**
   - Başlangıç otomatı gösterimi
   - Ön işleme sonrası otomat (yeni başlangıç/kabul durumlarıyla)
   - Her eliminasyon adımında güncel otomat durumu
   - Geçiş etiketlerinin regex olarak gösterilmesi

3. **Adım Adım İzleme**
   - Her eliminasyon adımında hangi durumun elimine edildiği
   - Güncellenen regex ifadeleri
   - Eliminasyon sırasının mantığı

4. **Sonuç**
   - Final Regular Expression
   - Regex'in sadeleştirilmiş hali (opsiyonel)
   - Test input'ları ile doğrulama

## ✅ Kabul Kriterleri

- [ ] State Elimination algoritması doğru implementa edilmeli
- [ ] NFA ve DFA input'ları kabul edilmeli
- [ ] Adım adım görselleştirme yapılmalı
- [ ] Her adımda regex ifadeleri gösterilmeli
- [ ] Final regex doğru olmalı (test edilebilir)
- [ ] UI Streamlit'te temiz ve anlaşılır olmalı
- [ ] Mevcut proje yapısına uygun modüler kod
- [ ] Edge case'ler handle edilmeli (boş dil, epsilon, tek durum, vb.)

## 📚 Teorik Arka Plan

### State Elimination Algoritması

State Elimination, bir finite automata'yı regular expression'a dönüştürmenin standart yöntemlerinden biridir.

**Ana Fikir:**
- Otomatı bir **Generalized NFA (GNFA)** gibi düşün
- GNFA'da geçişler tek sembol yerine regex ifadeleri olabilir
- Durumları teker teker elimine ederek regex'leri birleştir
- Sonunda sadece başlangıç → kabul arası tek bir regex kalır

### Örnek Dönüşüm

```
DFA:
  States: {q0, q1, q2}
  Start: q0
  Accept: {q2}
  Transitions:
    q0 --a--> q1
    q1 --b--> q2
    q0 --b--> q0
    q1 --a--> q1
    q2 --a--> q2
    q2 --b--> q2

Adımlar:
1. Ön işleme: Yeni start (s) ve accept (f) ekle
   s --ε--> q0
   q2 --ε--> f

2. q0'ı elimine et:
   s --a--> q1  (s-ε->q0-a->q1)
   s --b--> q0 çıkarılır (self-loop olur)

3. q1'i elimine et:
   ...

Son Regex: b*a(a)*b(a|b)*
```

## 🛠️ Implementasyon İpuçları

### Regex Gösterimi

Geçişleri bir dictionary ile tutabilirsiniz:

```python
transitions = {
    ('q0', 'q1'): 'a',
    ('q1', 'q2'): 'b',
    ('q0', 'q0'): 'b',
}

# Eliminasyon sonrası:
transitions = {
    ('q0', 'q2'): 'ab',  # q0->q1->q2 birleştirildi
    ('q0', 'q0'): 'b',
}
```

### Regex Simplification (Opsiyonel)

Bazı basitleştirmeler yapılabilir:
- `∅|a = a` (empty union)
- `ε·a = a` (epsilon concatenation)
- `a|a = a` (idempotent union)
- `(a*)* = a*` (nested stars)

Ancak genel simplification NP-hard bir problem olduğu için basit kurallarla sınırlı kalınabilir.

### Eliminasyon Sırasının Seçimi

Durum eliminasyon sırası sonucu etkilemez ama regex'in karmaşıklığını etkiler:

**Stratejiler:**
1. **Basit sıra:** Durumları sırayla elimine et
2. **En az bağlantılı:** Önce az geçişi olan durumları elimine et
3. **Manual selection:** Kullanıcıya sırayı seçtir (advanced özellik)

## 📚 Referanslar

- [State Elimination Method - Stanford](https://web.stanford.edu/class/archive/cs/cs103/cs103.1142/lectures/18/Small18.pdf)
- Sipser, Michael. "Introduction to the Theory of Computation" - Chapter 1.3
- [Visual explanation](https://www.youtube.com/watch?v=--CSVsFIDng)

## 💡 Test Örnekleri

### Örnek 1: Basit DFA

```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a", "b"],
  "transitions": {
    "q0": {"a": "q1", "b": "q0"},
    "q1": {"a": "q1", "b": "q1"}
  },
  "start_state": "q0",
  "accept_states": ["q1"]
}
```

**Beklenen Regex:** `a(a|b)*`

### Örnek 2: Kleene Star İçeren

```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a"],
  "transitions": {
    "q0": {"a": "q1"},
    "q1": {"a": "q0"}
  },
  "start_state": "q0",
  "accept_states": ["q1"]
}
```

**Beklenen Regex:** `(aa)*a` veya eşdeğeri

## 🎯 Gelişmiş Özellikler (Opsiyonel)

Temel implementasyondan sonra eklenebilecek özellikler:

- [ ] Regex simplification (basitleştirme)
- [ ] Kullanıcının eliminasyon sırasını seçmesi
- [ ] Çıktı regex'in minimize edilmesi
- [ ] Birden fazla kabul durumu desteği (direkt)
- [ ] Tersine dönüşüm testi (RE → ε-NFA → minimize → RE karşılaştırma)

## 👥 Katkıda Bulunmak İçin

1. Bu issue'yu kendinize assign edin
2. Feature branch oluşturun: `git checkout -b feature/automata-to-regex`
3. `automata/automata_to_regex.py` modülünü oluşturun
4. `app.py`'ye yeni menü seçeneğini ekleyin
5. Test edin ve pull request açın

Bu oldukça ilginç ve challenging bir algoritma! Sorularınız için issue altında tartışabiliriz. 🧠🚀
