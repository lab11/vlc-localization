
origin = 'center'

w = 28.0
l = 29.0

#position_of_transmitters = [-w/2*2.54 l/2*2.54 0; w/2*2.54 l/2*2.54 0; w/2*2.54 -l/2*2.54 0; -w/2*2.54 -l/2*2.54 0; 0 0 0];
#frequency_of_transmitter = [2000; 2500; 3000; 3500; 4000];

transmitters_from_paper_in_cm = {
        2000 : ((-w/2*2.54,  l/2*2.54, 0),),
        2500 : (( w/2*2.54,  l/2*2.54, 0),),
        3000 : (( w/2*2.54, -l/2*2.54, 0),),
        3500 : ((-w/2*2.54, -l/2*2.54, 0),),
        4000 : ((        0,         0, 0),),
        }

transmitters_from_zero_in_cm = {
        2000 : ((-w/2*2.54,  l/2*2.54, 246),),
        2500 : (( w/2*2.54,  l/2*2.54, 246),),
        3000 : (( w/2*2.54, -l/2*2.54, 246),),
        3500 : ((-w/2*2.54, -l/2*2.54, 246),),
        4000 : ((        0,         0, 246),),
        }

transmitters_zero_floor_in_m = {
        2000 : ((-w/2*.0254,  l/2*.0254, 2.46),),
        2500 : (( w/2*.0254,  l/2*.0254, 2.46),),
        3000 : (( w/2*.0254, -l/2*.0254, 2.46),),
        3500 : ((-w/2*.0254, -l/2*.0254, 2.46),),
        4000 : ((         0,          0, 2.46),),
        }

transmitters = transmitters_from_paper_in_cm
units = 'cm'
user_is = 'below'

transmitters = transmitters_from_zero_in_cm
units = 'cm'
user_is = 'below'

#transmitters = transmitters_zero_floor_in_m
#units = 'm'
#user_is = 'below'

