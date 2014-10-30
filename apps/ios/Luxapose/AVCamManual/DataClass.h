//
//  DataClass.h
//  VLC
//
//  Created by Noah Klugman on 8/20/14.
//  Copyright (c) 2014 Noah Klugman. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface DataClass : NSObject {
    NSString *server_name;
}

@property(nonatomic,retain)NSString *server_name;

+(DataClass*)getInstance;

@end

