//
//  DataClass.m
//  VLC
//
//  Created by Noah Klugman on 8/20/14.
//  Copyright (c) 2014 Noah Klugman. All rights reserved.
//

#import "DataClass.h"

@implementation DataClass

@synthesize server_name;

static DataClass *instance = nil;

+(DataClass *)getInstance
{
    @synchronized(self)
    {
        if(instance==nil)
        {
            instance= [DataClass new];
        }
    }
    return instance;
}

@end
