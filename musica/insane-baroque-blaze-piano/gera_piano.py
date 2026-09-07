# -*- coding: utf-8 -*-
"""Gera 'Insane Baroque Blaze' - versao simplificada para piano (primeiros 30 s).

Fonte das notas: transcricoes MIDI publicadas no laudo do tritono
(nandovalle.com/o-tritono/reproduzir): guitar_basic_pitch.mid,
guitar_anthemscore.mid e bass_basic_pitch.mid, analisadas em grade de
compasso a 148 bpm (4/4), com o primeiro tempo forte em t = 1,108 s.

Simplificacoes aplicadas:
  * sextinas de guitarra viram colcheias (mesmo arpejo, mesma direcao);
  * mao direita quase sempre em linha unica; acordes de 3 notas so no riff final;
  * mao esquerda em oitavas longas (semibreve/minima) e seminimas no riff;
  * compasso 18 e um acorde final de La maior sustentado (a faixa segue
    dali; e o ponto de corte dos 30 s).

Uso: python gera_piano.py  ->  insane-baroque-blaze-piano-simplificado.mid
"""
import mido
from mido import Message, MetaMessage, MidiFile, MidiTrack

BPM = 148
PPQ = 480
E = PPQ // 2          # colcheia
NOMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def n(nome):
    """'C#4' -> 61 ; 'Bb3' -> 58 ; 'R' -> None (pausa)."""
    if nome == 'R':
        return None
    letra, resto = nome[0], nome[1:]
    alt = 0
    while resto and resto[0] in '#b':
        alt += 1 if resto[0] == '#' else -1
        resto = resto[1:]
    return 12 * (int(resto) + 1) + NOMES[letra] + alt


def ev(nomes, colcheias):
    """Evento: uma nota ('C#4'), um acorde (['G#3','C#4','E4']) ou pausa 'R'."""
    if isinstance(nomes, str):
        nomes = [nomes]
    return ([n(x) for x in nomes if n(x) is not None], colcheias * E)


# ---------------------------------------------------------------- mao direita
RH = []
# --- Introducao: arpejo de Do# dim7 (Do#-Mi-Sol-La#), compassos 0-3
RH += [ev('A#3', 1), ev('C#4', 1), ev('G4', 1), ev('A#4', 1), ev('C#5', 1), ev('E5', 1), ev('G5', 1), ev('E5', 1)]        # c.0
RH += [ev(x, 1) for x in ['C#5', 'A#4', 'G4', 'E4', 'C#4', 'A#3', 'G3', 'E3']]                                            # c.1
RH += [ev(x, 1) for x in ['C#3', 'E3', 'G3', 'A#3', 'C#4', 'E4', 'G4', 'A#4']]                                            # c.2
RH += [ev(x, 1) for x in ['C#5', 'E5', 'G5', 'E5', 'C#5', 'A#4', 'G4', 'E4']]                                             # c.3
# --- Pedal de Sol#: arpejo Sol#-Si-Re-Fa, compassos 4-5
RH += [ev(x, 1) for x in ['C#4', 'B3', 'G3', 'B3', 'D4', 'F4', 'G#4', 'B4']]                                              # c.4
RH += [ev(x, 1) for x in ['D5', 'F5', 'G#5', 'F5', 'D5', 'B4', 'D5', 'B4']]                                               # c.5
# --- Tema, compassos 6-12
RH += [ev('C#5', 4), ev('C#4', 1), ev('E4', 1), ev('G#4', 1), ev('C#5', 1)]                                               # c.6  Do#m
RH += [ev('D#5', 2), ev('C#5', 1), ev('D#5', 1), ev('G#4', 1), ev('D#5', 1), ev('E5', 1), ev('F#5', 1)]                   # c.7  Do#m(maj7)/Do
RH += [ev('D#5', 1), ev('F#5', 1), ev('E5', 1), ev('C#5', 1), ev('D#5', 2), ev('C#5', 2)]                                 # c.8  Do#m
RH += [ev('E5', 2), ev('C#5', 1), ev('E5', 1), ev('D#5', 1), ev('E5', 1), ev('F#5', 2)]                                   # c.9  La | Si
RH += [ev('G#5', 4), ev('E5', 1), ev('B4', 1), ev('E5', 1), ev('G#5', 1)]                                                 # c.10 Mi
RH += [ev('A5', 2), ev('G#5', 1), ev('F#5', 1), ev('E5', 1), ev('D#5', 1), ev('F#5', 1), ev('E5', 1)]                     # c.11 Sol#
RH += [ev('G#5', 2), ev('E5', 1), ev('C#5', 1), ev('F#4', 1), ev('E4', 1), ev('C#4', 1), ev('E4', 1)]                     # c.12 Do#m
# --- Sequencia Re#7b9 -> Sol#7b9, compassos 13-14
RH += [ev(x, 1) for x in ['D#4', 'G4', 'A#4', 'C#5', 'E5', 'C#5', 'C#5', 'D#5']]                                          # c.13 Re#7b9
RH += [ev('E5', 1), ev('D#5', 1), ev('C5', 1), ev('A4', 1), ev('F#4', 1), ev('D#4', 1), ev('C4', 2)]                      # c.14 Sol#7b9
# --- Riff de acordes, compassos 15-17
CSm_sus = ['G#3', 'C#4', 'D#4']; CSm = ['G#3', 'C#4', 'E4']
GS_BS = ['G#3', 'C4', 'D#4']; GS7 = ['F#3', 'G#3', 'D#4']; E_GS = ['G#3', 'B3', 'E4']
RH += [ev(CSm_sus, 1)] * 2 + [ev(CSm, 1)] * 6                                                                             # c.15 Do#m
RH += [ev(GS_BS, 1)] * 6 + [ev(GS7, 1)] * 2                                                                               # c.16 Sol#/Si#
RH += [ev(CSm, 1)] * 6 + [ev(E_GS, 1)] * 2                                                                                # c.17 Do#m -> Mi/Sol#
RH += [ev(['A3', 'C#4', 'E4'], 8)]                                                                                        # c.18 La (corte)

# ---------------------------------------------------------------- mao esquerda
def oit(nome, colcheias):
    p = n(nome)
    return ([p, p + 12], colcheias * E)

LH = []
LH += [oit('C#2', 8)] * 2                        # c.0-1  Do# (tonica)
LH += [oit('G1', 8)] * 2                         # c.2-3  Sol (pedal do tritono, como no baixo original)
LH += [oit('G#1', 8), oit('G#1', 4), oit('G#1', 4)]  # c.4-5  Sol# (dominante)
LH += [oit('C#2', 4), oit('C#2', 4)]             # c.6
LH += [oit('C2', 4), oit('C2', 4)]               # c.7
LH += [oit('C#2', 4), oit('C#2', 4)]             # c.8
LH += [oit('A1', 4), oit('B1', 4)]               # c.9
LH += [oit('E2', 4), oit('E2', 4)]               # c.10
LH += [oit('G#1', 4), oit('G#1', 4)]             # c.11
LH += [oit('C#2', 4), oit('C#2', 4)]             # c.12
LH += [oit('D#2', 4), oit('D#2', 4)]             # c.13
LH += [oit('G#1', 4), oit('G#1', 4)]             # c.14
LH += [oit('C#2', 2)] * 4                        # c.15
LH += [oit('C2', 2)] * 4                         # c.16
LH += [oit('C#2', 2)] * 3 + [oit('B1', 2)]       # c.17
LH += [oit('A1', 8)]                             # c.18


def escreve_trilha(nome, eventos, canal, vel, legato=0.9):
    tr = MidiTrack()
    tr.append(MetaMessage('track_name', name=nome, time=0))
    tr.append(Message('program_change', program=0, channel=canal, time=0))
    pend = 0  # ticks acumulados de pausa
    for pitches, dur in eventos:
        if not pitches:
            pend += dur
            continue
        on = int(dur * legato)
        for i, p in enumerate(pitches):
            tr.append(Message('note_on', note=p, velocity=vel, channel=canal, time=pend if i == 0 else 0))
            pend = 0
        for i, p in enumerate(pitches):
            tr.append(Message('note_off', note=p, velocity=0, channel=canal, time=on if i == 0 else 0))
        pend = dur - on
    tr.append(MetaMessage('end_of_track', time=pend))
    return tr


mid = MidiFile(ticks_per_beat=PPQ)
meta = MidiTrack()
meta.append(MetaMessage('track_name', name='Insane Baroque Blaze - piano simplificado (0:00-0:30)', time=0))
meta.append(MetaMessage('copyright', text='Nando Valle - arranjo simplificado para piano', time=0))
meta.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM), time=0))
meta.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
meta.append(MetaMessage('key_signature', key='C#m', time=0))
meta.append(MetaMessage('end_of_track', time=0))
mid.tracks.append(meta)
mid.tracks.append(escreve_trilha('Mao direita', RH, 0, 92))
mid.tracks.append(escreve_trilha('Mao esquerda', LH, 1, 78, legato=0.95))

saida = 'insane-baroque-blaze-piano-simplificado.mid'
mid.save(saida)
rh_t = sum(d for _, d in RH); lh_t = sum(d for _, d in LH)
assert rh_t == lh_t == 19 * 8 * E, (rh_t / (8 * E), lh_t / (8 * E))
print(f'ok: {saida}  {rh_t / (8 * E):.0f} compassos  {mid.length:.1f} s')
