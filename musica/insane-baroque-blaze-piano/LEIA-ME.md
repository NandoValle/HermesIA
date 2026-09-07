# Insane Baroque Blaze — versão simplificada para piano (0:00–0:30)

Arranjo para piano dos primeiros 30 segundos de **Insane Baroque Blaze**
(Nando Valle, 2026, ISRC QZNJV2617176), reduzido para nível intermediário.

| Arquivo | O que é |
|---|---|
| `insane-baroque-blaze-piano-simplificado.mid` | O arranjo: 2 trilhas (mão direita / mão esquerda), 148 bpm, 4/4, Dó# menor, 19 compassos, 30,7 s |
| `gera_piano.py` | Gera o `.mid` acima (`pip install mido` e `python gera_piano.py`) |
| `piano-roll.svg` | Prévia visual do arranjo |

## De onde vieram as notas

Das transcrições MIDI publicadas no laudo do trítono
(`nandovalle.com/o-tritono/reproduzir`): `guitar_basic_pitch.mid`,
`guitar_anthemscore.mid` e `bass_basic_pitch.mid`. Os três arquivos foram
lidos numa grade de compasso a 148 bpm, com o primeiro tempo forte em 1,108 s
da gravação. As alturas de cada compasso vêm do consenso entre os dois
transcritores de guitarra; o baixo definiu a harmonia.

Aviso honesto: as transcrições são automáticas e trazem notas fantasmas e
oitavas trocadas. A introdução (c. 0–5) e o riff (c. 15–17) são bem nítidos
nas duas fontes. O tema (c. 6–14) foi lido de material mais ruidoso, então
notas isoladas dessa parte podem diferir do que a guitarra toca na gravação.
Confira de ouvido.

## Simplificações

- As sextinas da guitarra viraram colcheias (mesmo arpejo, mesma direção).
  A 148 bpm dá 5 notas por segundo na mão direita.
- Mão direita em linha única, exceto no riff de acordes (3 notas).
- Mão esquerda em oitavas longas (semibreves e mínimas) e seminimas no riff.
- O compasso 18 é um acorde de Lá sustentado: é onde a faixa foi cortada
  aos 30 s (a gravação segue a partir dali).

## Estrutura

| Compasso | Tempo na gravação | Harmonia | Mão direita |
|---|---|---|---|
| 0–1 | 0:01–0:04 | Dó# dim7 (pedal Dó#) | Arpejo Dó#–Mi–Sol–Lá# subindo até Sol5 e descendo até Mi3 |
| 2–3 | 0:04–0:07 | pedal de Sol no baixo (trítono da tônica, como na gravação) | Arpejo dim7 sobe de Dó#3 a Sol5 e desce |
| 4–5 | 0:07–0:11 | pedal de Sol# | Arpejo Sol#–Si–Ré–Fá sobe e desce |
| 6–8 | 0:11–0:15 | Dó#m · Dó#m(maj7)/Dó · Dó#m | Tema em torno de Dó#5–Ré#5–Fá#5 |
| 9–10 | 0:15–0:19 | Lá · Si · Mi | Tema sobe a Sol#5 |
| 11–12 | 0:19–0:22 | Sol# · Dó#m | Descida de Lá5 até Dó#4 |
| 13–14 | 0:22–0:25 | Ré#7♭9 · Sol#7♭9 | Arpejo sobe (Ré#) e desce (Sol#) até Dó4 |
| 15–17 | 0:25–0:30 | Dó#m · Sol#/Si# · Dó#m → Mi/Sol# | Acordes em colcheias |
| 18 | 0:30 | Lá | Acorde final sustentado |
