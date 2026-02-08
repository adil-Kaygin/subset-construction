---
name: RE Karşılaştırma Paneli
about: İki Regular Expression'ı DFA'ya dönüştürüp karşılaştıran panel eklenmesi
title: '[FEATURE] RE Karşılaştırma Paneli - İki RE'yi DFA Üzerinden Karşılaştırma'
labels: ['enhancement', 'good first issue', 'help wanted']
assignees: ''
---

## 🎯 Özellik Açıklaması

Kullanıcıların iki farklı Regular Expression (RE) girerek bunları DFA'ya dönüştürüp karşılaştırabilecekleri bir panel eklenmesi.

## 📋 Detaylı Gereksinimler

### Dönüşüm Akışı
İki Regular Expression için aşağıdaki dönüşüm pipeline'ı uygulanacak:

```
RE_1 → ε-NFA_1 → DFA_1
RE_2 → ε-NFA_2 → DFA_2
```

Ardından `DFA_1` ve `DFA_2` karşılaştırılacak.

### UI/UX Gereksinimleri

1. **Giriş Alanları**
   - İki ayrı text input alanı (RE_1 ve RE_2 için)
   - Regex syntax yardımcısı (desteklenen operatörler: `|`, `*`, `+`, `?`, `()`)
   - Örnek regex'ler için dropdown/öneriler

2. **Dönüşüm Gösterimi**
   - Her iki RE için ayrı ayrı dönüşüm adımlarını gösterme
   - RE → ε-NFA görselleştirmesi
   - ε-NFA → DFA görselleştirmesi (Lazy Subset Construction)
   - Her adımda ara sonuçların gösterilmesi

3. **Karşılaştırma Sonuçları**
   - İki DFA'nın eşdeğer olup olmadığı
   - Eşdeğer değilse, karşı örnek string gösterimi
   - Alt küme ilişkisi varsa bunu belirtme (L(DFA_1) ⊆ L(DFA_2) veya tersi)
   - Symmetric difference gösterimi

4. **Görselleştirme**
   - Her iki DFA'nın yan yana görselleştirilmesi
   - Eşdeğer durumların highlight edilmesi (varsa)
   - İnteraktif graf keşfi

## 🔧 Teknik Detaylar

### Kullanılacak Mevcut Modüller

Projede zaten aşağıdaki modüller mevcut ve kullanılabilir:

1. **`automata/regex_to_nfa.py`**: Thompson Construction ile RE → ε-NFA
2. **`automata/lazy_subset.py`**: ε-NFA → DFA dönüşümü
3. **`automata/comparison.py`**: İki DFA'nın karşılaştırılması
4. **`automata/visualizer.py`**: Automata görselleştirme

### Yeni Eklenecek Kod

`app.py` dosyasına yeni bir menü seçeneği eklenecek:

```python
# Menü seçeneklerine eklenecek:
"5️⃣ RE Karşılaştırma"
```

### Örnek Kullanım Senaryosu

```python
# Kullanıcı girişi
RE_1 = "(a|b)*abb"
RE_2 = "(a|b)*abb"

# Dönüşüm
converter = RegexToNFA()
epsilon_nfa_1 = converter.convert(RE_1)
epsilon_nfa_2 = converter.convert(RE_2)

# ε-NFA → DFA
lazy_1 = LazySubsetConstruction(epsilon_nfa_1)
dfa_1 = lazy_1.convert()

lazy_2 = LazySubsetConstruction(epsilon_nfa_2)
dfa_2 = lazy_2.convert()

# Karşılaştırma
comparator = DFAComparison(dfa_1, dfa_2)
is_equivalent, steps = comparator.are_equivalent()
```

## ✅ Kabul Kriterleri

- [ ] Kullanıcı iki RE girebilmeli
- [ ] Her iki RE için dönüşüm adımları görselleştirilmeli
- [ ] Sonuçta elde edilen DFA'lar karşılaştırılmalı
- [ ] Eşdeğerlik sonucu açık bir şekilde gösterilmeli
- [ ] Eşdeğer değilse, karşı örnek string gösterilmeli
- [ ] Tüm görselleştirmeler Streamlit UI'da düzgün çalışmalı
- [ ] Kod mevcut proje yapısına uygun olmalı (modüler ve clean)
- [ ] Hata durumları düzgün handle edilmeli (invalid regex, etc.)

## 📚 Referanslar

- Mevcut DFA Karşılaştırma implementasyonu: `automata/comparison.py`
- Mevcut Regex → ε-NFA implementasyonu: `automata/regex_to_nfa.py`
- Thompson Construction: [Wikipedia](https://en.wikipedia.org/wiki/Thompson%27s_construction)
- Hopcroft-Karp DFA Minimization algoritması

## 💡 İpuçları

1. `app.py` dosyasındaki mevcut menü yapısına benzer şekilde yeni bir sekme ekleyin
2. Streamlit'in `st.columns()` fonksiyonunu kullanarak iki sütunlu layout oluşturabilirsiniz
3. Her dönüşüm adımını `st.expander()` ile göstererek kullanıcıya adım adım takip imkanı sunabilirsiniz
4. Mevcut `comparison.py` modülünü inceleyin - zaten DFA karşılaştırma mantığı hazır

## 🎨 Örnek UI Tasarımı

```
┌─────────────────────────────────────────────────────────┐
│              RE Karşılaştırma Paneli                    │
├─────────────────────┬───────────────────────────────────┤
│  RE_1 Input         │  RE_2 Input                       │
│  (a|b)*abb          │  (a|b)*ab                         │
├─────────────────────┼───────────────────────────────────┤
│  RE_1 → ε-NFA_1     │  RE_2 → ε-NFA_2                   │
│  [Graf Gösterimi]   │  [Graf Gösterimi]                 │
├─────────────────────┼───────────────────────────────────┤
│  ε-NFA_1 → DFA_1    │  ε-NFA_2 → DFA_2                  │
│  [Graf Gösterimi]   │  [Graf Gösterimi]                 │
├─────────────────────┴───────────────────────────────────┤
│           Karşılaştırma Sonuçları                       │
│                                                          │
│  ❌ DFA'lar eşdeğer değil                               │
│  Karşı örnek: "ab"                                       │
│  - DFA_1 kabul ediyor: ❌                                │
│  - DFA_2 kabul ediyor: ✅                                │
└──────────────────────────────────────────────────────────┘
```

## 👥 Katkıda Bulunmak İçin

1. Bu issue'yu kendinize assign edin
2. Feature branch oluşturun: `git checkout -b feature/regex-comparison`
3. Değişikliklerinizi commit edin
4. Pull request açın

Sorularınız varsa issue altında tartışabiliriz! 🚀
