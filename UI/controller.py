import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._album = None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        durataStr = self._view._txtInDurata.value
        if not durataStr:
            self._view.create_alert('Inserire una durata!')
            return
        if not durataStr.isdigit():
            self._view.create_alert('Inserire una durata intera!')
            return
        durata = int(durataStr)
        n, ed = self._model.buildGraph(durata)
        self._view.txt_result.controls.append(ft.Text(f'Creato grafo con {n} nodi e {ed} archi', color='green'))

        self._view._ddAlbum.options = list(map(lambda al:ft.dropdown.Option(key=str(al), data=al, on_click=self.getSelectedAlbum), self._model.getAlbums()))

        self._view.update_page()

    def getSelectedAlbum(self, e):
        self._album = e.control.data

    def handleAnalisiComp(self, e):
        if not self._album:
            self._view.create_alert('Seleziona un album!')
            return
        dim, dur = self._model.getInfoConnessa(self._album)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f'Trovata componente connessa formata da {dim} album, con durata totale di {dur} minuti'))
        self._view.update_page()


    def handleGetSetAlbum(self, e):
        pass