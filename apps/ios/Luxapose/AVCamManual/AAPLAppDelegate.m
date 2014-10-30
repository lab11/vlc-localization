/*
 Copyright (C) 2014 Apple Inc. All Rights Reserved.
 See LICENSE.txt for this sample’s licensing information
 
 Abstract:
 
  Application delegate.
  
 */

#import "AAPLAppDelegate.h"
#import "AAPLCameraViewController.h"
#import <CoreLocation/CoreLocation.h>

@interface AAPLAppDelegate()<CLLocationManagerDelegate>

@property (strong, nonatomic) CLBeaconRegion *beaconRegion;
@property (strong, nonatomic) NSUUID *beaconUUID;
@property (strong, nonatomic) NSString *regionIdentifier;
@property (strong, nonatomic) CLLocationManager *locationManager;

@end


@implementation AAPLAppDelegate

@synthesize beaconRegion, beaconUUID, regionIdentifier;

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    /*
    self.locationManager = [[CLLocationManager alloc] init];
    self.locationManager.delegate = self;
    if([self.locationManager respondsToSelector:@selector(requestAlwaysAuthorization)]) {
        [self.locationManager requestAlwaysAuthorization];
    }
    self.locationManager.pausesLocationUpdatesAutomatically = NO;
    
    beaconUUID = [[NSUUID alloc] initWithUUIDString:@"01122334-4556-6778-899A-ABBCCDDEEFF0"];
    regionIdentifier = @"us.umich";
    
    beaconRegion = [[CLBeaconRegion alloc] initWithProximityUUID:beaconUUID major:1 minor:232 identifier:regionIdentifier];
    beaconRegion.notifyOnEntry = YES;
    beaconRegion.notifyOnExit = YES;
    beaconRegion.notifyEntryStateOnDisplay = YES;
    
    switch ([CLLocationManager authorizationStatus]) {
        case kCLAuthorizationStatusAuthorizedAlways:
            NSLog(@"Authorized Always");
            break;
        case kCLAuthorizationStatusAuthorizedWhenInUse:
            NSLog(@"Authorized when in use");
            break;
        case kCLAuthorizationStatusDenied:
            NSLog(@"Denied");
            break;
        case kCLAuthorizationStatusNotDetermined:
            NSLog(@"Not determined");
            break;
        case kCLAuthorizationStatusRestricted:
            NSLog(@"Restricted");
            break;
        default:
            break;
    }
    
    //if (!beaconRegion) {
    //    NSLog(@"NIL");
    //}
    
    [self.locationManager startMonitoringForRegion:beaconRegion];
    [self.locationManager startRangingBeaconsInRegion:beaconRegion];
    [self.locationManager startUpdatingLocation];

    NSSet *setOfRegions = [self.locationManager monitoredRegions];
    for (CLRegion *region in setOfRegions) {
        NSLog (@"region info: %@", region);
    }

    
    //[self.locationManager startMonitoringForRegion:beaconRegion];
    //[self.locationManager startUpdatingLocation];
    
    NSLog(@"DONE");
    */
    return YES;
}

-(void)locationManager:(CLLocationManager *)manager didEnterRegion:(CLBeaconRegion *)region {
    
    [manager startRangingBeaconsInRegion:(CLBeaconRegion*)region];
    [self.locationManager startUpdatingLocation];
    
    NSLog(@"You entered the region.");
    [self sendLocalNotificationWithMessage:@"You entered the region."];
    
}

-(void)locationManager:(CLLocationManager *)manager didExitRegion:(CLBeaconRegion *)region {
    
    [manager stopRangingBeaconsInRegion:(CLBeaconRegion*)region];
    [self.locationManager stopUpdatingLocation];
    
    NSLog(@"You exited the region.");
    [self sendLocalNotificationWithMessage:@"You exited the region."];
    
}

-(void)sendLocalNotificationWithMessage:(NSString*)message {
    /*
    [[UIApplication sharedApplication] registerUserNotificationSettings:[UIUserNotificationSettings settingsForTypes:(UIUserNotificationTypeSound | UIUserNotificationTypeAlert | UIUserNotificationTypeBadge) categories:nil]];
    [[UIApplication sharedApplication] registerForRemoteNotifications]; // you can also set here for local notification.
    
    UILocalNotification *notification = [[UILocalNotification alloc] init];
    notification.alertBody = message;
    [[UIApplication sharedApplication] scheduleLocalNotification:notification];
    */
}

 

-(void)locationManager:(CLLocationManager *)manager didMonitorBeacons:(NSArray *)beacons inRegion:
(CLRegion *)region {
    NSLog(@"HIT 2");

}


- (void)locationManager:(CLLocationManager *)manager monitoringDidFailForRegion:(CLRegion *)region withError:(NSError *)error
{
 
    NSLog (@"region info: %@", region);
    
    // It is nice to monitor errors...
    NSLog(@"monitoringDidFailForRegion - error: %@", [error localizedDescription]);
}

-(BOOL)CanDeviceSupportAppBackgroundRefresh
{
    // Override point for customization after application launch.
    if ([[UIApplication sharedApplication] backgroundRefreshStatus] == UIBackgroundRefreshStatusAvailable) {
        NSLog(@"Background updates are available for the app.");
        return YES;
    }else if([[UIApplication sharedApplication] backgroundRefreshStatus] == UIBackgroundRefreshStatusDenied)
    {
        NSLog(@"The user explicitly disabled background behavior for this app or for the whole system.");
        return NO;
    }else if([[UIApplication sharedApplication] backgroundRefreshStatus] == UIBackgroundRefreshStatusRestricted)
    {
        NSLog(@"Background updates are unavailable and the user cannot enable them again. For example, this status can occur when parental controls are in effect for the current user.");
        return NO;
    }
    return YES;
}


-(void)locationManager:(CLLocationManager *)manager didRangeBeacons:(NSArray *)beacons inRegion:
    (CLRegion *)region {
    
    //NSLog(@"HIT");
    NSString *message = @"";
    
    AAPLCameraViewController *viewController = (AAPLCameraViewController*)self.window.rootViewController;
    viewController.beacons = beacons;
    [viewController.tableView reloadData];
    
    if(beacons.count > 0) {
        CLBeacon *nearestBeacon = beacons.firstObject;
        if(nearestBeacon.proximity == self.lastProximity ||
           nearestBeacon.proximity == CLProximityUnknown) {
            return;
        }
        self.lastProximity = nearestBeacon.proximity;
        
        switch(nearestBeacon.proximity) {
            case CLProximityFar:
                message = @"You are far away from the beacon";
                break;
            case CLProximityNear:
                message = @"You are near the beacon";
                break;
            case CLProximityImmediate:
                message = @"You are in the immediate proximity of the beacon";
                break;
            case CLProximityUnknown:
                return;
        }
    } else {
        message = @"No beacons are nearby";
    }
    NSLog(@"%@", message);
    
     //[self sendLocalNotificationWithMessage:message];s
}


@end


