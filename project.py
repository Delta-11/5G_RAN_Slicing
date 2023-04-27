import numpy as np
import matplotlib.pyplot as plt
import random
import math
import time

#-------------------------------------------Function for Allocation------------------------------------------------------------------------------
def allocation_fun(closest_base_station, base_station, user_slice_needed, user_bw_required):
  if base_station[closest_base_station].max_users < base_station[closest_base_station].current_users:
    print("Maximum user limit reached for BS, so cannot be served at this moment")
  else:
    print("Chances are request might be served based on the availability of resources")
    #Check if user slice is eMBB
    if user_slice_needed == 'eMBB':
      #Check no of active_(Slice) user is less than max_(Slice) user
      if base_station[closest_base_station].active_eMBB < base_station[closest_base_station].max_eMBB:
        #Check if user bw required is less than current bw available
        if user_bw_required < base_station[closest_base_station].current_bw: 
          #Allocate the BW to user
          print("User request for the corresponding slice with the required Bandwidth is served")
          #Parameters to be changed or updated after allocation
          #Increase the current user for that BS by 1
          base_station[closest_base_station].current_users = base_station[closest_base_station].current_users + 1
          # Decrease the user BW from the current BW available at that BS 
          base_station[closest_base_station].current_bw = base_station[closest_base_station].current_bw - user_bw_required
          # Increase the active no of user for eMBB slice by 1
          base_station[closest_base_station].active_eMBB = base_station[closest_base_station].active_eMBB + 1
          return True

        #Check if user bw can be served using reserved bw + current bw
        elif user_bw_required <= (base_station[closest_base_station].current_bw + base_station[closest_base_station].reserved_bw):
          #Allocate BW to user using reserved BW
          print("User request for the corresponding slice with the required Bandwidth is served but using reserved bandwidth")
          # Parameters to be changed after the allocation of BW
          #Increase the current user for that BS by 1
          base_station[closest_base_station].current_users = base_station[closest_base_station].current_users + 1
          # Increase the active no of user for eMBB slice by 1
          base_station[closest_base_station].active_eMBB = base_station[closest_base_station].active_eMBB + 1
          # Decrease the user BW from the current BW and also from reserved BW available at that BS
          # Assume c_bw = 30 and r_bw = 20 so p_c_bw = 30
          base_station[closest_base_station].partial_current_bw = base_station[closest_base_station].current_bw
          # c_bw = 0 i.e all current_bw is used so we need to use reserved bw
          base_station[closest_base_station].current_bw = 0
          # p_r_bw = 45 - 30 = 15
          base_station[closest_base_station].partial_reserved_bw = user_bw_required - base_station[closest_base_station].partial_current_bw
          # r_bw = 20 - 15 = 5 i.e only 5 units is reserved and rest 15 is allocated
          base_station[closest_base_station].reserved_bw = base_station[closest_base_station].reserved_bw - base_station[closest_base_station].partial_reserved_bw
          return True
        
        else:
          print("We cannot serve you using our reserved bandwidth also")
          return False
      else:
        print("We cannot serve you because the number of active user for eMBB slice is more than the BS can serve at a time, Let me check if we can connect to other BS")
        return False

      #Check if user slice is uRLLC
    elif user_slice_needed == 'uRLLC':
      #Check no of active_(Slice) user is less than max_(Slice) user
      if base_station[closest_base_station].active_uRLLC < base_station[closest_base_station].max_uRLLC:
        #Check if user bw required is less than current bw available
        if user_bw_required < base_station[closest_base_station].current_bw: 
          #Allocate the BW to user
          print("User request for the corresponding slice with the required Bandwidth is served")
          #Parameters to be changed or updated after allocation
          #Increase the current user for that BS by 1
          base_station[closest_base_station].current_users = base_station[closest_base_station].current_users + 1
          # Decrease the user BW from the current BW available at that BS 
          base_station[closest_base_station].current_bw = base_station[closest_base_station].current_bw - user_bw_required
          # Increase the active no of user for uRLLC slice by 1
          base_station[closest_base_station].active_uRLLC = base_station[closest_base_station].active_uRLLC + 1
          return True

        #Check if user bw can be served using reserved bw + current bw
        elif user_bw_required <= (base_station[closest_base_station].current_bw + base_station[closest_base_station].reserved_bw):
          #Allocate BW to user using reserved BW
          print("User request for the corresponding slice with the required Bandwidth is served but using reserved bandwidth")
          # Parameters to be changed after the allocation of BW
          #Increase the current user for that BS by 1
          base_station[closest_base_station].current_users = base_station[closest_base_station].current_users + 1
          # Increase the active no of user for uRLLC slice by 1
          base_station[closest_base_station].active_uRLLC = base_station[closest_base_station].active_uRLLC + 1
          # Decrease the user BW from the current BW and also from reserved BW available at that BS
          # Assume c_bw = 30 and r_bw = 20 so p_c_bw = 30
          base_station[closest_base_station].partial_current_bw = base_station[closest_base_station].current_bw
          # c_bw = 0 i.e all current_bw is used so we need to use reserved bw
          base_station[closest_base_station].current_bw = 0
          # p_r_bw = 45 - 30 = 15
          base_station[closest_base_station].partial_reserved_bw = user_bw_required - base_station[closest_base_station].partial_current_bw
          # r_bw = 20 - 15 = 5 i.e only 5 units is reserved and rest 15 is allocated
          base_station[closest_base_station].reserved_bw = base_station[closest_base_station].reserved_bw - base_station[closest_base_station].partial_reserved_bw
          return True
        
        else:
          print("We cannot serve you using our reserved bandwidth also")
          return False
      else:
        print("We cannot serve you because the number of active user for uRLLC slice is more than the Base Station can serve at a time, Let me check if we can connect to other BS")
        return False

      #Check if user slice is mMTC
    elif user_slice_needed == 'mMTC':
      #Check no of active_(Slice) user is less than max_(Slice) user
      if base_station[closest_base_station].active_mMTC < base_station[closest_base_station].max_mMTC:
        #Check if user bw required is less than current bw available
        if user_bw_required < base_station[closest_base_station].current_bw: 
          #Allocate the BW to user
          print("User request for the corresponding slice with the required Bandwidth is served")
          #Parameters to be changed or updated after allocation
          #Increase the current user for that BS by 1
          base_station[closest_base_station].current_users = base_station[closest_base_station].current_users + 1
          # Decrease the user BW from the current BW available at that BS 
          base_station[closest_base_station].current_bw = base_station[closest_base_station].current_bw - user_bw_required
          # Increase the active no of user for mMTC slice by 1
          base_station[closest_base_station].active_mMTC = base_station[closest_base_station].active_mMTC + 1
          return True

        #Check if user bw can be served using reserved bw + current bw
        elif user_bw_required <= (base_station[closest_base_station].current_bw + base_station[closest_base_station].reserved_bw):
          #Allocate BW to user using reserved BW
          print("User request for the corresponding slice with the required Bandwidth is served but using reserved bandwidth")
          # Parameters to be changed after the allocation of BW
          #Increase the current user for that BS by 1
          base_station[closest_base_station].current_users = base_station[closest_base_station].current_users + 1
          # Increase the active no of user for uRLLC slice by 1
          base_station[closest_base_station].active_mMTC = base_station[closest_base_station].active_mMTC + 1
          # Decrease the user BW from the current BW and also from reserved BW available at that BS
          # Assume c_bw = 30 and r_bw = 20 so p_c_bw = 30
          base_station[closest_base_station].partial_current_bw = base_station[closest_base_station].current_bw
          # c_bw = 0 i.e all current_bw is used so we need to use reserved bw
          base_station[closest_base_station].current_bw = 0
          # p_r_bw = 45 - 30 = 15
          base_station[closest_base_station].partial_reserved_bw = user_bw_required - base_station[closest_base_station].partial_current_bw
          # r_bw = 20 - 15 = 5 i.e only 5 units is reserved and rest 15 is allocated
          base_station[closest_base_station].reserved_bw = base_station[closest_base_station].reserved_bw - base_station[closest_base_station].partial_reserved_bw
          return True
        
        else:
          print("We cannot serve you using our reserved bandwidth also")
          return False
      else:
        print("We cannot serve you because the number of active user for mMTC slice is more than the Base Station can serve at a time, Let me check if we can connect to other BS")
        return False



#------------------------------------------Function for Deallocation of Slices--------------------------------------------------------------------------
def deallocation_fun(closest_base_station, base_station, user_slice_needed, user_bw_required):
  #----------------------------eMBB slice Deallocation----------------------------------------------------------------------
  if user_slice_needed == 'eMBB':
    if base_station[closest_base_station].current_bw + user_bw_required <= base_station[closest_base_station].static_current_bw:
      base_station[closest_base_station].current_bw = base_station[closest_base_station].current_bw + user_bw_required
      #Parameters to be changed or updated after allocation
      #Decrease the current user for that BS by 1
      base_station[closest_base_station].current_users = base_station[closest_base_station].current_users - 1
      # Decrease the active no of user for eMBB slice by 1
      base_station[closest_base_station].active_eMBB = base_station[closest_base_station].active_eMBB - 1
    else:
      base_station[closest_base_station].reserved_bw = base_station[closest_base_station].reserved_bw + ((base_station[closest_base_station].current_bw + user_bw_required) - base_station[closest_base_station].static_current_bw)
      base_station[closest_base_station].partial_reserved_bw = base_station[closest_base_station].partial_reserved_bw - ((base_station[closest_base_station].current_bw + user_bw_required) - base_station[closest_base_station].static_current_bw)
      base_station[closest_base_station].current_bw = user_bw_required - ((base_station[closest_base_station].current_bw + user_bw_required) - base_station[closest_base_station].static_current_bw)
      base_station[closest_base_station].partial_current_bw = base_station[closest_base_station].partial_current_bw - base_station[closest_base_station].current_bw 
      #Parameters to be changed or updated after allocation
      #Decrease the current user for that BS by 1
      base_station[closest_base_station].current_users = base_station[closest_base_station].current_users - 1
      # Decrease the active no of user for eMBB slice by 1
      base_station[closest_base_station].active_eMBB = base_station[closest_base_station].active_eMBB - 1



  #----------------------------uRLLC slice Deallocation----------------------------------------------------------------------
  if user_slice_needed == 'uRLLC':
    if base_station[closest_base_station].current_bw + user_bw_required <= base_station[closest_base_station].static_current_bw:
      base_station[closest_base_station].current_bw = base_station[closest_base_station].current_bw + user_bw_required
      #Parameters to be changed or updated after allocation
      #Decrease the current user for that BS by 1
      base_station[closest_base_station].current_users = base_station[closest_base_station].current_users - 1
      # Decrease the active no of user for uRLLC slice by 1
      base_station[closest_base_station].active_uRLLC = base_station[closest_base_station].active_uRLLC - 1
    else:
      base_station[closest_base_station].reserved_bw = base_station[closest_base_station].reserved_bw + ((base_station[closest_base_station].current_bw + user_bw_required) - base_station[closest_base_station].static_current_bw)
      base_station[closest_base_station].partial_reserved_bw = base_station[closest_base_station].partial_reserved_bw - ((base_station[closest_base_station].current_bw + user_bw_required) - base_station[closest_base_station].static_current_bw)
      base_station[closest_base_station].current_bw = user_bw_required - ((base_station[closest_base_station].current_bw + user_bw_required) - base_station[closest_base_station].static_current_bw)
      base_station[closest_base_station].partial_current_bw = base_station[closest_base_station].partial_current_bw - base_station[closest_base_station].current_bw 
      #Parameters to be changed or updated after allocation
      #Decrease the current user for that BS by 1
      base_station[closest_base_station].current_users = base_station[closest_base_station].current_users - 1
      # Decrease the active no of user for uRLLC slice by 1
      base_station[closest_base_station].active_uRLLC = base_station[closest_base_station].active_uRLLC - 1


  #----------------------------mMTC slice Deallocation----------------------------------------------------------------------
  if user_slice_needed == 'mMTC':
    if base_station[closest_base_station].current_bw + user_bw_required <= base_station[closest_base_station].static_current_bw:
      base_station[closest_base_station].current_bw = base_station[closest_base_station].current_bw + user_bw_required
      #Parameters to be changed or updated after allocation
      #Decrease the current user for that BS by 1
      base_station[closest_base_station].current_users = base_station[closest_base_station].current_users - 1
      # Decrease the active no of user for mMTC slice by 1
      base_station[closest_base_station].active_mMTC = base_station[closest_base_station].active_mMTC - 1
    else:
      base_station[closest_base_station].reserved_bw = base_station[closest_base_station].reserved_bw + ((base_station[closest_base_station].current_bw + user_bw_required) - base_station[closest_base_station].static_current_bw)
      base_station[closest_base_station].partial_reserved_bw = base_station[closest_base_station].partial_reserved_bw - ((base_station[closest_base_station].current_bw + user_bw_required) - base_station[closest_base_station].static_current_bw)
      base_station[closest_base_station].current_bw = user_bw_required - ((base_station[closest_base_station].current_bw + user_bw_required) - base_station[closest_base_station].static_current_bw)
      base_station[closest_base_station].partial_current_bw = base_station[closest_base_station].partial_current_bw - base_station[closest_base_station].current_bw 
      #Parameters to be changed or updated after allocation
      #Decrease the current user for that BS by 1
      base_station[closest_base_station].current_users = base_station[closest_base_station].current_users - 1
      # Decrease the active no of user for uRLLC slice by 1
      base_station[closest_base_station].active_mMTC = base_station[closest_base_station].active_mMTC - 1




#----------------------------------------User Intialization (Take data from the user and return the corresponding requirement)--------------------------------------------------------------------
def user_data(ue_bs_min_dist, flag, required_id, user_slice):
  if flag == 0:
    ueid = int(input("User Id(0-100):"))
    user_bw_required = int(input("User Bandwidth Requirement: "))
    user_slice_needed = input("Slice Type: ")
    ue = User(ueid, user_coordx[ueid], user_coordy[ueid], user_bw_required, user_slice_needed) # User with id = 0 , loc = (x,y) with 50 units of BW requirement in 'eMBB' slice
    #ue_obj_list.append(ue)
    print("User Slice Requirement",user_slice_needed)
    print("User BW Required",user_bw_required)
    # print("id =", ue.id, "Coordinates=(",ue.bs_x,",",ue.bs_y,")","Bandwidth Required=",ue.bw_required,"SliceType:",ue.slice_type)

    # 2. Get the closest base station to the User (ex- id=0)
    local_closest_base_station = ue_bs_min_dist[ueid]
    print("Closest BS to the ueid that you gave is" , local_closest_base_station)
    return [ueid, user_bw_required, user_slice_needed, local_closest_base_station]

  elif flag == 1:
    #ueid = int(input("User Id(0-100):"))
    user_bw_required = int(input("Enter New Bandwidth Requirement: "))
    #user_slice_needed = input("Slice Type: ")
    ue = User(required_id, user_coordx[required_id], user_coordy[required_id], user_bw_required, user_slice) # User with id = 0 , loc = (x,y) with 50 units of BW requirement in 'eMBB' slice
    #ue_obj_list.append(ue)
    print("User Slice Requirement",user_slice)
    print("New BW Required",user_bw_required)
    # print("id =", ue.id, "Coordinates=(",ue.bs_x,",",ue.bs_y,")","Bandwidth Required=",ue.bw_required,"SliceType:",ue.slice_type)

    # 2. Get the closest base station to the User (ex- id=0)
    local_closest_base_station = ue_bs_min_dist[required_id]
    #print("Closest BS to the ueid that you gave is" , local_closest_base_station)
    return [required_id, user_bw_required, user_slice, local_closest_base_station]



#----------------------------Intialize the function and also call the allocation function--------------------------------------------
def user_intial_fun(flag, required_id, user_slice):
  ue_list = user_data(ue_bs_min_dist, flag, required_id, user_slice)
  ueid = ue_list[0]
  user_bw_required = ue_list[1]
  user_slice_needed = ue_list[2]
  closest_base_station_three = ue_list[3]
  closest_base_station = -1

  check = True # Set check to true
  for i in range(0,3):
    if i == 0 and check == True:
      closest_base_station = closest_base_station_three[i]
      print("---------------------Before Allocation---------------------")
      print_status(closest_base_station, base_station, user_slice_needed)
      check = allocation_fun(closest_base_station, base_station, user_slice_needed, user_bw_required)
      if check == False:
        continue
      print("---------------------After Allocation---------------------")
      print_status(closest_base_station, base_station, user_slice_needed)
      return [closest_base_station, user_slice_needed, user_bw_required, ueid]

    elif check == False:
      closest_base_station = closest_base_station_three[i]
      check = allocation_fun(closest_base_station, base_station, user_slice_needed, user_bw_required)
      if check == True:
        print("---------------------After Allocation---------------------")
        print_status(closest_base_station, base_station, user_slice_needed)
        return [closest_base_station, user_slice_needed, user_bw_required, ueid]
      else:
        continue
  
  if closest_base_station == -1:
    print("Cannot allocate any of the 3 closest base station to the UE with ueid = ",ueid, "at the moment")
    #id = ue_obj_list.pop()
    return [-1,-1,-1, ueid]


#------------------------------------------Switch Case Function------------------------------------------

def switch_case(argument, ue_obj_list):
#Logic Handlinf for SLA at admission
  if argument == 'C':
    #flag=0
    print("Connection working")
    user_intial_list = user_intial_fun(0, -1, 'XYZ') #returns list of variables
    closest_base_station = user_intial_list[0] # list[0] contains closest_base_station to which ue got connected, if not -1
    user_slice_needed = user_intial_list[1] # list[1] contains type of User Slice
    user_bw_required = user_intial_list[2] # list[2] contains Bandwidth required by the user
    ueid = user_intial_list[3] # list[3] contains user id 
    print("Allocated Successfully UE:", ueid, "BS: ", closest_base_station)
    if closest_base_station != -1:
      ue_obj_list.append(user_intial_list)

    return user_intial_list

  elif argument == 'D':
    print("Disconnection working")
    disconnect_id = int(input("Enter the UEid that you want to disconnect : "))
    for i in range(len(ue_obj_list)):
      if disconnect_id == ue_obj_list[i][3]:
        closest_base_station = ue_obj_list[i][0] # incomplete, check how to get closest_base_station
        user_slice_needed = ue_obj_list[i][1]
        user_bw_required = ue_obj_list[i][2]
        deallocation_fun(closest_base_station, base_station, user_slice_needed, user_bw_required)
        print("Deallocated successfully UE:",disconnect_id, "BS: ",closest_base_station)


#Logic for SLA handling when BW Requirement is changed by the user
  elif argument == 'S':
    #flag=1
    print("Allocating new requirement wait.......")
    required_id = int(input("Enter the UEid whose requirement you want to change: "))
    for i in range(len(ue_obj_list)):
      if required_id == ue_obj_list[i][3]:
        closest_base_station = ue_obj_list[i][0]
        user_slice_needed = ue_obj_list[i][1]
        user_bw_required = ue_obj_list[i][2]
        deallocation_fun(closest_base_station, base_station, user_slice_needed, user_bw_required)

        user_intial_list = user_intial_fun(1, required_id, user_slice_needed)
        closest_base_station = user_intial_list[0] # list[0] contains closest_base_station to which ue got connected, if not -1
        user_slice_needed = user_intial_list[1] # list[1] contains type of User Slice
        user_bw_required = user_intial_list[2] # list[2] contains Bandwidth required by the user
        ueid = user_intial_list[3] # list[3] contains user id 
        print("Allocated Successfully with New Requirement UE:", ueid, "BS: ", closest_base_station)
        if closest_base_station != -1:
          ue_obj_list.append(user_intial_list)

        return user_intial_list

      else:
        print("Invalid id ")


  elif argument == 'exit':
    print("Stopping the simulation")

  else:
    print("Invalid argument")

#------------------------------------------(Printing Status)-----------------------------------------------------------------------------
def print_status(closest_base_station, base_station, user_slice_needed):
  if user_slice_needed == 'eMBB':
    print("Active eMBB user in a Base Station:",base_station[closest_base_station].active_eMBB)
    print("Max eMBB user in a Base Station:",base_station[closest_base_station].max_eMBB)
  elif user_slice_needed == 'uRLLC':
    print("Active uRLLC user in a Base Station:",base_station[closest_base_station].active_uRLLC)
    print("Max uRLLC user in a Base Station:",base_station[closest_base_station].max_uRLLC)
  elif user_slice_needed == 'mMTC':
    print("Active mMTC user in a Base Station:",base_station[closest_base_station].active_mMTC)
    print("Max mMTC user in a Base Station:",base_station[closest_base_station].max_mMTC)

  print("Current User in a Base Station :",base_station[closest_base_station].current_users)
  print("Current BW Available : ",base_station[closest_base_station].current_bw)
  print("Reserved BW Available : ",base_station[closest_base_station].reserved_bw)
  print("Partial Current BW Available : ",base_station[closest_base_station].partial_current_bw)
  print("Partial Reserved BW Available : ",base_station[closest_base_station].partial_reserved_bw)
  print("-------------------------------------------------------------")

#-----------------Area of a Square------------------------------------------------------------------------
def square_area(x1, y1, x2, y2, x3, y3, x4, y4):

    side = x2 - x1
    area = side * side
    return area

area = square_area(0, 0, 15, 0, 0, 15, 15, 15)
#print(area)

#---------------------Calculate x,y coordinates of a Base Station-----------------------------------------
n = 25 # number of points (Base Station)

a = np.random.uniform(low = 0, high = 15, size = 25)
b = np.random.uniform(low = 0, high = 15, size = 25)

# x,y coordinates of 25 base station
bs_coordx = [int(i) for i in a]
bs_coordy = [int(i) for i in b]

# print(coordx)
# print(coordy)

#----------------------------------------------------------------------------------------------------------
# Resource Element
# class resource_element:
#   def __init__(self, modulation_scheme, quality) -> None:
#     self.m_s = modulation_scheme
#     self.q = quality

#----------------------Base Station Class------------------------------------------------------------------
# Base Station Class
# Assumptions 100 resource blocks , 4 x 4 MIMO in downlink with 20MHz channel bandwidth in FDD mode, with 64 QAM (6 bits/symbol) the throughput will be 300Mbps
class BaseStation:
  def __init__(self, x, y, max_users, current_users, total_bw, current_bw, reserved_bw, static_current_bw, static_reserved_bw, partial_current_bw, partial_reserved_bw, active_eMBB, active_uRLLC, active_mMTC, max_eMBB, max_uRLLC, max_mMTC) -> None:
      self.bs_x = x # x coord of base station 's'
      self.bs_y = y # y coord of base station 's'
      self.max_users = max_users # max no of users allowed per base station 's' 
      self.current_users = current_users # total no of users available per base station 's' (including all slices) 
      self.total_bw = total_bw # total bw available in base station 's'
      self.current_bw = current_bw # shows current bw available
      self.reserved_bw = reserved_bw # bw reserved for future use
      self.static_current_bw = static_current_bw #Initial current_bw, it's not going to change
      self.static_reserved_bw = static_reserved_bw #Initial reserved_bw, it's not going to change
      self.partial_current_bw = partial_current_bw # How much partial current_bw is used when allocating with reserved BW 
      self.partial_reserved_bw = partial_reserved_bw # How much partial reserved_bw is used when allocating with reserved BW
      self.active_eMBB = active_eMBB # active no of users for eMBB slice type in BS 's'
      self.active_uRLLC = active_uRLLC # active no of users for uRLLC slice type in BS 's'
      self.active_mMTC = active_mMTC # active no of users for mMTC slice type in BS 's'
      self.max_eMBB = max_eMBB # max no of users for eMBB slice type per BS 's'
      self.max_uRLLC = max_uRLLC # max no of users for uRLLC slice type per BS 's'
      self.max_mMTC = max_mMTC # max no of users for mMTC slice type per BS 's'



#------------------User Class-----------------------------------------------------------------------------
class User:
  def __init__(self, ueid, x, y, bw_required, slice_type) -> None:
      self.id = ueid
      self.bs_x = x # x coord of user 'u'
      self.bs_y = y # y coord of user 'u'
      self.bw_required = bw_required # BW requirement from the user
      self.slice_type = slice_type # Slice type from user



base_station = [] # base_station list stores BS object for each BS 
for i in range(0,25):
  #(x, y, max_users, current_users, total_bw, current_bw, reserved_bw, static_current_bw, static_reserved_bw, partial_current_bw, partial_reserved_bw, active_eMBB, active_uRLLC, active_mMTC, max_eMBB, max_uRLLC, max_mMTC)
  bs_obj = BaseStation(bs_coordx[i], bs_coordy[i], random.randint(20,30), 0, 100, 80, 20, 80, 20, 0, 0, 0, 0, 0, 10, 7, 3)
  base_station.append(bs_obj)

#------------------------Starting of the program flow (main function)-------------------------------------
#----------------------Total No of users across area or BS------------------------------------------------
#Calculate total no of users spread across all base station
total_users=0
max_user_per_bs = [] #Maximum no of user a single BS(0-24) can serve
for i in range(0,25):
  total_users = total_users + base_station[i].max_users
  max_user_per_bs.append(base_station[i].max_users)

print("Total Users across all BS: ",total_users)

#----------------------Graph Plotting----------------------------------------------------------------------

a1 = np.random.uniform(low = 0, high = 15, size = total_users)
b1 = np.random.uniform(low = 0, high = 15, size = total_users)

fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(111)

ax1.scatter(a1, b1, s=10, c='r', marker="s", label='UE')
ax1.scatter(a, b, s=30, c='b', marker="s", label='BS')
plt.legend(loc='upper left')
plt.show()

# ------------------X,Y coordinates of each user----------------------------------------------------------
user_coordx = [int(i) for i in a1] # user_coordx is a list that store 'x' coordinates of all users
user_coordy = [int(i) for i in b1] # user_coordy is a list that store 'y' coordinates of all users

# print(user_coordx)
# print(user_coordy)

#---------------Find distance of a UE from all the base station-------------------------------------------
temp_dist_list = []
ue_bs_min_dist = [] #Stores 3 closest BS from each UE(0 to totalusers-1)
for j in range(0,total_users):
  for i in range(0,25):
    ue = [user_coordx[j], user_coordy[j]]
    bs = [bs_coordx[i],bs_coordy[i]]
    temp_dist = math.dist(ue, bs) 
    temp_dist_list.append(temp_dist)
  #---------------Finding base station closer to UE-------------------------------------------------------
  min_index_list = []
  #---------------------------------First BS(index) closer to UE ------------------------------------------
  first_min_dist = min(temp_dist_list) # Minimum dist from the list stored in first_min_dist
  first_min_index = temp_dist_list.index(first_min_dist) #find the Index of first_min_dist
  min_index_list.append(first_min_index) # Index stored in the list
  temp_dist_list.remove(first_min_dist) # Remove the 1st minimum from the list


  #---------------------------------Second BS(index) closer to UE----------------------------------------
  second_min_dist = min(temp_dist_list) # Minimum dist from the list stored in first_min_dist
  second_min_index = temp_dist_list.index(second_min_dist) #find the Index of first_min_dist
  min_index_list.append(second_min_index) # Index stored in the list
  temp_dist_list.remove(second_min_dist) # Remove the 1st minimum from the list

  #---------------------------------Third BS(index) closer to UE--------------------------------------------
  third_min_dist = min(temp_dist_list) # Minimum dist from the list stored in first_min_dist
  third_min_index = temp_dist_list.index(third_min_dist) #find the Index of first_min_dist
  min_index_list.append(third_min_index) # Index stored in the list
  temp_dist_list.remove(third_min_dist) # Remove the 1st minimum from the list

  ue_bs_min_dist.append(min_index_list) # Stores the list of index of a 3 BS which is closer to UE
  temp_dist_list.clear()
print("Index of all BS that is closer to UE starting from 0-(total_user - 1)\n",ue_bs_min_dist)



# #-------------------------User Allocation to the Base Station--------------------------------------------

# ueid_list = [] # Stores the list of all ueid return by user_data()
ue_obj_list = [] # Stores the UE obj (we are storing the order in which the request comes, we will process based on that)
# user_bw_required_list = [] # Stores the bw_required for all user
# user_slice_needed_list = [] # Stores the user_slice_needed for all user
# closest_base_station_list = [] # Stores the closest_base_station for all the user

# for i in range(50):
#   closest_base_station_list.append(0)
#   ueid_list.append(0)
#   user_bw_required_list.append(0)
#   user_slice_needed_list.append(0)




#------------------------------Collect the data from user_intial_function and call with the user data and check if it can be allocated or not-------------------------------------
# user_intial_list = user_intial_fun() #returns list of variables
# closest_base_station = user_intial_list[0] # list[0] contains closest_base_station to which 
# user_slice_needed = user_intial_list[1] # list[1] contains type of User Slice
# user_bw_required = user_intial_list[2] # list[2] contains Bandwidth required by the user
# ueid = user_intial_list[3] # list[3] contains user id 

#---------------------------Simulation Part-------------------------------------------
while(1):
  ip = input("Enter 'C' for Connect, 'D' for Disconnect, 'S' for staying connected and requirement change and 'exit' for exiting : ")
  data_list = switch_case(ip,ue_obj_list)

  if ip == 'C' or ip == 'D' or ip == 'S':
    time.sleep(20)

  elif ip == 'exit':
    break

  else:
    continue



#------------------------------------------------------------------------------------------------------
# print("---------------------Before De-Allocation---------------------")
# print_status(closest_base_station, base_station, user_slice_needed)

# deallocation_fun(closest_base_station, base_station, user_slice_needed, user_bw_required)

# print("---------------------After De-Allocation---------------------")
# print_status(closest_base_station, base_station, user_slice_needed)



