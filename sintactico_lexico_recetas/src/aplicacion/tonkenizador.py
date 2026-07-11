import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from aplicacion.estrategias.estrategia_automata import EstrategiaAutomata
from aplicacion.estrategias.estrategia_diccionario import EstrategiaDiccionario


class Tokenizador:
    def __init__(self, estrategia_automata: EstrategiaAutomata = None,
                 estrategia_diccionario: EstrategiaDiccionario = None):
        self.estrategia_automata = estrategia_automata or EstrategiaAutomata()
        self.estrategia_diccionario = estrategia_diccionario or EstrategiaDiccionario()

    def tokenizar(self, texto: str) -> dict:
        inicio_total = time.perf_counter()

        matches_afd = self._correr_afd(texto)

        fragmentos_nl = {}
        cursor = 0
        for _, inicio, fin in matches_afd:
            frag = texto[cursor:inicio].strip()
            if frag:
                fragmentos_nl[cursor] = frag
            cursor = fin
        frag_final = texto[cursor:].strip()
        if frag_final:
            fragmentos_nl[cursor] = frag_final

        eventos_dic = []
        if fragmentos_nl:
            with ThreadPoolExecutor(max_workers=len(fragmentos_nl), thread_name_prefix='DIC-') as ejecutor:
                futuros = {
                    ejecutor.submit(self.estrategia_diccionario.tokenizar_con_posiciones, frag): pos
                    for pos, frag in fragmentos_nl.items()
                }
                for futuro in as_completed(futuros):
                    offset = futuros[futuro]
                    for token, pos_relativa in futuro.result():
                        eventos_dic.append((offset + pos_relativa, token))

        eventos = [(pos, tok) for pos, tok in eventos_dic]
        eventos += [(inicio, tok) for tok, inicio, _ in matches_afd]
        eventos.sort(key=lambda e: e[0])

        tokens_final = [tok for _, tok in eventos]

        tiempo_total = time.perf_counter() - inicio_total
        hilos_concurrentes = 1 + len(fragmentos_nl)

        return {
            'tokens': tokens_final,
            'tiempo_total_segundos': round(tiempo_total, 4),
            'hilos_concurrentes': hilos_concurrentes,
            'oracion_original': texto,
        }

    def _correr_afd(self, texto: str):
        return self.estrategia_automata.tokenizar_con_posiciones(texto)