from manim import UP, FadeIn, FadeOut

from componentes import grafo_decorativo, logo_esquina

from . import (
    cerrar_rama,
    cierre,
    configuracion,
    conventional_commits,
    conflictos,
    el_problema,
    era_ia,
    fork_y_pr,
    git_amend,
    git_checkout,
    git_diff,
    git_fetch_y_pull,
    git_ignore,
    git_init,
    git_push,
    git_reflog,
    git_remote,
    git_reset,
    git_revert,
    historia,
    instalacion,
    la_terminal,
    local_remoto,
    log,
    merge,
    mensajes_commit,
    minecraft,
    portada,
    pronto_iniciamos,
    que_es_git,
    que_es_un_commit,
    ramas,
    rebase_y_cherry,
    siguientes_pasos,
    tres_zonas,
)


class SlideBase:
    def indicador(self):
        if getattr(self, "_indicador", None) is None:
            self._indicador = logo_esquina()
        return self._indicador

    def next_slide(self, *args, indicador=True, **kwargs):
        if not indicador:
            super().next_slide(*args, **kwargs)
            return
        logo = self.indicador()
        self.play(FadeIn(logo, shift=UP * 0.1), run_time=0.3)
        super().next_slide(*args, **kwargs)
        self.remove(logo)

    def iniciar_slide(self):
        self._slide_actual = getattr(self, "_slide_actual", 0) + 1
        marco = getattr(self, "marco", None)
        fondo_viejo = getattr(self, "_fondo", None)
        resto = [m for m in self.mobjects if m is not marco and m is not fondo_viejo]
        for m in resto:
            m.clear_updaters()

        self._fondo = grafo_decorativo(self._slide_actual - 1)
        salidas = [FadeOut(m) for m in resto]
        if fondo_viejo is not None:
            salidas.append(FadeOut(fondo_viejo))
        self.play(*salidas, FadeIn(self._fondo))
        if marco is not None:
            self.add(marco)


def _slide(construir):
    def metodo(self):
        self.iniciar_slide()
        construir(self)

    return metodo


class SlidesInicio:
    slide_pronto_iniciamos = _slide(pronto_iniciamos.construir)
    slide_portada = _slide(portada.construir)
    slide_el_problema = _slide(el_problema.construir)


class SlidesFundamentos:
    slide_que_es_git = _slide(que_es_git.construir)
    slide_minecraft = _slide(minecraft.construir)
    slide_historia = _slide(historia.construir)
    slide_era_ia = _slide(era_ia.construir)
    slide_la_terminal = _slide(la_terminal.construir)
    slide_instalacion = _slide(instalacion.construir)
    slide_configuracion = _slide(configuracion.construir)


class SlidesLocal:
    slide_git_init = _slide(git_init.construir)
    slide_tres_zonas = _slide(tres_zonas.construir)
    slide_que_es_un_commit = _slide(que_es_un_commit.construir)
    slide_log = _slide(log.construir)
    slide_mensajes_commit = _slide(mensajes_commit.construir)
    slide_conventional_commits = _slide(conventional_commits.construir)
    slide_git_ignore = _slide(git_ignore.construir)
    slide_git_diff = _slide(git_diff.construir)
    slide_git_reset = _slide(git_reset.construir)
    slide_git_checkout = _slide(git_checkout.construir)
    slide_git_revert = _slide(git_revert.construir)
    slide_git_amend = _slide(git_amend.construir)
    slide_git_reflog = _slide(git_reflog.construir)


class SlidesRamas:
    slide_ramas = _slide(ramas.construir)
    slide_merge = _slide(merge.construir)
    slide_conflictos = _slide(conflictos.construir)
    slide_cerrar_rama = _slide(cerrar_rama.construir)


class SlidesRemoto:
    slide_local_remoto = _slide(local_remoto.construir)
    slide_git_remote = _slide(git_remote.construir)
    slide_git_push = _slide(git_push.construir)
    slide_git_fetch_y_pull = _slide(git_fetch_y_pull.construir)
    slide_fork_y_pr = _slide(fork_y_pr.construir)


class SlidesFinal:
    slide_rebase_y_cherry = _slide(rebase_y_cherry.construir)
    slide_siguientes_pasos = _slide(siguientes_pasos.construir)
    slide_cierre = _slide(cierre.construir)
