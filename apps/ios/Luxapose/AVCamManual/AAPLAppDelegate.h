/*
 Copyright (C) 2014 Apple Inc. All Rights Reserved.
 See LICENSE.txt for this sample’s licensing information
 
 Abstract:
 
  Application delegate.
  
*/

@import UIKit;
#import <CoreLocation/CoreLocation.h>

@interface AAPLAppDelegate : UIResponder <UIApplicationDelegate, CLLocationManagerDelegate>




@property (nonatomic) UIWindow *window;
@property CLProximity lastProximity;

@end
