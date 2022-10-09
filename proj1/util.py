def orderCoordinates(quadrilateral):
    # https://pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/

    # Top Left, Top Right, Bottom Left, Bottom Right
    # TL --- TR
    # |      |
    # |      |
    # BL --- BR
    coords = quadrilateral.verticesCoords
    
    sumCoords = [[coords[i][0] + coords[i][1], coords[i][1] - coords[i][0], coords[i]] for i in range(len(coords))]
    sumCoords.sort(key = lambda x: (x[0], x[1]))
    
    topLeft = sumCoords[0]
    topRight = sumCoords[1]
    bottomLeft = sumCoords[2]
    bottomRight = sumCoords[3]

    # Horizontal Oriented
    if quadrilateral.width >= 1.2 * quadrilateral.height:
        return [topLeft[2], topRight[2], bottomLeft[2], bottomRight[2]]
    # Vertical Oriented
    elif quadrilateral.width <= 0.8 * quadrilateral.height:
        return [bottomLeft[2], topLeft[2], bottomRight[2], topRight[2]]
    # Diamond Oriented
    else:
        if bottomLeft[1] < topRight[1]:
            return [topLeft[2], bottomLeft[2], topRight[2], bottomRight[2]]
        else:
            return [topRight[2], topLeft[2], bottomRight[2], bottomLeft[2]]

        #      3,0
        # 0,3       6,3
        #      3, 6

        #     3,0 -> TL
        #          7,2 -> BL
        # 1,4 -> TR
        #       5,6 -> BR   

        #     3,0 -> TL
        # 1,2 -> TR       
        #           7,4 -> BL
        #       5,6 -> BR   
