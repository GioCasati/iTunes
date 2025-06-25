from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAlbums(durataMin):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT a.*, SUM(t.Milliseconds)/1000/60 as dTot
                   FROM Album a, Track t
                   WHERE a.AlbumId = t.AlbumId
                   GROUP BY a.AlbumId
                   HAVING dTot > %s"""

        cursor.execute(query, (durataMin,))
        res = []
        for row in cursor.fetchall():
            res.append(Album(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllEdges(durataMin):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()

        query = """SELECT DISTINCT p1.AlbumId, p2.AlbumId
                    FROM 
                        (SELECT a.AlbumId , p.TrackId, p.PlaylistId
                        FROM album a , track t , playlisttrack p 
                        WHERE a.AlbumId = t.AlbumId and t.TrackId = p.TrackId
                            AND a.AlbumId IN (SELECT a.AlbumId
                                               FROM Album a, Track t
                                               WHERE a.AlbumId = t.AlbumId
                                               GROUP BY a.AlbumId
                                               HAVING SUM(t.Milliseconds) > %s *1000*60)) p1,
                        (SELECT a.AlbumId , p.TrackId, p.PlaylistId
                        FROM album a , track t , playlisttrack p 
                        WHERE a.AlbumId = t.AlbumId and t.TrackId = p.TrackId
                            AND a.AlbumId IN (SELECT a.AlbumId
                                               FROM Album a, Track t
                                               WHERE a.AlbumId = t.AlbumId
                                               GROUP BY a.AlbumId
                                               HAVING SUM(t.Milliseconds) > %s *1000*60)) p2
                    WHERE p1.TrackId != p2.TrackId AND p1.AlbumId < p2.AlbumId AND p1.PlaylistId = p2.PlaylistId"""

        cursor.execute(query, (durataMin,durataMin))
        res = []
        for row in cursor.fetchall():
            res.append(row)

        cursor.close()
        cnx.close()
        return res