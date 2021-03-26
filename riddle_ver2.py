import numpy as np
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')
from mpl_toolkits.mplot3d import Axes3D
from numpy.random import rand
from pylab import figure

counter=0
from mpl_toolkits.mplot3d import Axes3D


def check_state(build_matrix):
    """
    if the state is out of range return false

    go through all the matrix and check the maximum difference between all parts in the same axis.

    :return: false- if the shape is wrong, true - if it is not out of range
    """
    size_of_cube_we_want_to_build=3
    print(build_matrix.shape)
    shape=build_matrix.shape
    x_length=shape[0]
    y_length = shape[1]
    z_length = shape[2]
    z_min = None
    z_max = None
    # go through the z axis
    for x in range(x_length):
        for y in range(y_length):
            for z in range(z_length):
                point=build_matrix[x][y][z]
                if point!=0:
                    if z_max==None:
                        z_max=z
                    if z_min==None:
                        z_min=z

                    if z>z_max:
                        z_max=z
                    if z<z_min:
                        z_min=z
    print(z_max,z_min)
    if z_max!= None and z_min!=None:
        if z_max-z_min>=size_of_cube_we_want_to_build:
            return False

    # go through the y axis
    y_min = None
    y_max = None
    for x in range(x_length):
        for z in range(z_length):
            for y in range(y_length):
                point=build_matrix[x][y][z]
                if point != 0:
                    if y_max == None:
                        y_max = y
                    if y_min == None:
                        y_min = y

                    if y > y_max:
                        y_max = y
                    if y < y_min:
                        y_min = y

    # go through the x axis
    x_min = None
    x_max = None
    print(y_max,y_min)
    if y_max!= None and y_min!=None:
        if y_max-y_min>=size_of_cube_we_want_to_build:
            return False

    for y in range(y_length):
        for z in range(z_length):
            for x in range(x_length):
                point=build_matrix[x][y][z]
                if point != 0:
                    if x_max == None:
                        x_max = x
                    if x_min == None:
                        x_min = x

                    if x > x_max:
                        x_max = x
                    if x < x_min:
                        x_min = x
    print(x_max, x_min)
    if x_max != None and x_min != None:
        if x_max - x_min >= size_of_cube_we_want_to_build:
            return False

    return True

def trying_to_assamble(orgenize,cube,axis,last_position): #axsis is xy or yz or xz
    """
    try to add part in some direction if it succeed it calls itself
    if when calling himself he get false then he tries the next direction he can
    if it doesnt succeed it tries in other direction, if it fails in all directions it return false
    copy objects because when they changed inside of function they changed also outside

    :param orgenize: matrix_build
    :param cube: the parts of the cube orgenized by list
    :param axis: current axis to add parts
    :param last_position: last position
    :return: true - if succeeded to solve , false - did'nt succeed
    """
    # check if it succeeded
    last_position_copy=last_position.copy()
    cube_copy=cube.copy()
    if len(cube_copy)<1:
        draw(orgenize)
    if cube_copy==[]:
        draw(orgenize)
        print("done")
        return True
    # delete part of the pieces that it build from them the big cube
    current_part=cube_copy[0]
    del cube_copy[0]
    for i in range(4):
        current_try=orgenize.copy()
        current_try_orgenize,new_last_position, is_it_possible=add_part(current_try,current_part,axis,i,last_position_copy,17-len(cube_copy))
        new_axis = get_current_axis(axis,i)
        if check_state(current_try_orgenize)==True and is_it_possible:
            print("going forword")
            #draw(current_try_orgenize)
            if trying_to_assamble(current_try_orgenize,cube_copy,new_axis,new_last_position)== True:
                return True
        else:
            #draw(current_try_orgenize)
            print("didnt succseed")
    print("going backwords")
    check_state(orgenize)
    #draw(current_try_orgenize)
    return False

def draw(organize):
    """
    draw all the points whos value is greater then 0 and write there's number besides them
    :param organize: matrix
    :return:
    """
    # draw the 3d plot of the cubes and number them by there's value
    # numbering of the figure
    global counter
    fig = plt.figure(counter)
    counter+=1
    #z, x, y = organize.nonzero()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(x, y, -z, zdir='z', c='red')
    ax = Axes3D(fig)
    shape = organize.shape
    x_length = shape[0]
    y_length = shape[1]
    z_length = shape[2]
    # go through all the matrix and paint the relevant points
    for x in range(x_length):
        for y in range(y_length):
            for z in range(z_length):
                point = organize[x][y][z]
                if point!=0:
                    ax.scatter(x,y,z,color='r')
                    ax.text(x,y,z, '%s' % (str(point)), size=20, zorder=1,
                            color='k')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()


def get_current_axis(old_axis,old_direction):
    """
    after adding a little cube the axis of the movement changes.
    the following function describe the new axis available for movements.
    it is decided by the old axis and the direction you chose to go

    :param old_axis: old axis used, for example 'xy'
    :param old_direction: between 0-3, direction is defined in add_part
    :return:
    """
    if old_axis=='xy':
        if old_direction==0 or old_direction==2:
            return 'yz'
        else:
            return 'xz'
    if old_axis=='yz':
        if old_direction == 0 or old_direction == 2:
            return 'xz'
        else:
            return 'xy'

    if old_axis=='xz':
        if old_direction == 0 or old_direction == 2:
            return 'yz'
        else:
            return 'xy'



def add_part(orgenize,current_part_size,axis,direction,last_position,part_number):
    """
    do: add part to orgenize in the place chosen,
    get axis and number of parts to add, add them in the direction got.
    it know where to add them because it gets the last position.

    :param orgenize: build of the matrix
    :param current_part_size: number of little cubes to add
    :param axis: axis to add in the little cube (contains combination of 2 axis for example: 'xy')
    :param direction: direction chosen for advancing (between 0-4)
    :param last_position: last position
    :param part_number: it marked the number of the action so it will be easy to retrace the program actions.
    :return: new matrix, new last position, state of success

    state of success:

    in case of not being able to add return False
    else return True
    """
    #
    new_position=[0,0,0]
    if axis=='xy':
        if direction==0:
            new_position[0]=1
        if direction==1:
            new_position[1]=1
        if direction==2:
            new_position[0]=-1
        if direction==3:
            new_position[1]=-1
    if axis=='yz':
        if direction==0:
            new_position[1]=1
        if direction==1:
            new_position[2]=1
        if direction==2:
            new_position[1]=-1
        if direction==3:
            new_position[2]=-1
    if axis=='xz':
        if direction==0:
            new_position[0]=1
        if direction==1:
            new_position[2]=1
        if direction==2:
            new_position[0]=-1
        if direction==3:
            new_position[2]=-1

    new_last_position=[]
    # add all parts
    for i in range(current_part_size):
        # check if there is already little cube in the chosen posion
        if orgenize[last_position[0]+new_position[0]*(i+1)][last_position[1]+new_position[1]*(i+1)][last_position[2]+new_position[2]*(i+1)]>=1:
            return orgenize,new_last_position,False
        # add part
        orgenize[last_position[0]+new_position[0]*(i+1)][last_position[1]+new_position[1]*(i+1)][last_position[2]+new_position[2]*(i+1)]=part_number
        new_last_position = [last_position[0]+new_position[0]*(i+1),last_position[1]+new_position[1]*(i+1),last_position[2]+new_position[2]*(i+1)]
    return orgenize,new_last_position,True

cube=[3,1,1,2,1,2,1,1,2,2,1,1,1,2,2,2,2]
orgenize= np.zeros((12,12,12))
print(orgenize)
trying_to_assamble(orgenize,cube,'xy',[5,5,5])

