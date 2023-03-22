def convertToAuthorsJson(authors):
    jsonData = []
    if len(authors) > 0:
        for i in authors:
            jsonData.append(
                {"id": i[0], "name": i[2], "hindex": i[3], "i10index": i[4], "imgUrl": i[5], "resource": i[6]}
            )
    return jsonData
