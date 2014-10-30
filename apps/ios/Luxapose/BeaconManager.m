//
//  BeaconManager.m
//  AVCamManual
//
//  Created by Noah Klugman on 8/26/14.
//  Copyright (c) 2014 Apple Inc. All rights reserved.
//

#import "BeaconManager.h"
#import "AAPLAppDelegate.h"

@interface BeaconManager()<CLLocationManagerDelegate>

@property (nonatomic, strong) CLLocationManager *locationManager;
@property (nonatomic, strong) CLBeaconRegion *beaconRegion;

@end

@implementation BeaconManager

+ (id)sharedManager
{
    static BeaconManager *sharedBeaconManager = nil;
    static dispatch_once_t once;
    dispatch_once(&once, ^{
        sharedBeaconManager = [[self alloc] init];
    });
    return sharedBeaconManager;
}

- (id)init
{
    self = [super init];
    if(self)
    {
        self.locationManager = [[CLLocationManager alloc] init];
        self.locationManager.delegate = self;
    }
    return self;
}

- (void)startBeaconMonitoring:(NSString*)forUUID
{
    NSUUID * uuid = [[NSUUID alloc] initWithUUIDString:forUUID];
    
    self.beaconRegion = [[CLBeaconRegion alloc] initWithProximityUUID:uuid identifier:@"com.beacons.publicRegion"];
    [self.locationManager startMonitoringForRegion:self.beaconRegion];
    [self.locationManager startRangingBeaconsInRegion:self.beaconRegion];
}

- (void)stopBeaconMonitoring
{
    //Stop the region monitoring
    if(self.locationManager != nil && self.beaconRegion != nil) {
        [self.locationManager stopRangingBeaconsInRegion:self.beaconRegion];
    }
}

#pragma mark - CLLocationManagerDelegate

- (void)locationManager:(CLLocationManager *)manager didRangeBeacons:(NSArray *)beacons inRegion:(CLBeaconRegion *)region
{
    self.beacons = beacons;
    if(self.delegate != nil) {
        [self.delegate beaconManager:self didRangeBeacons:self.beacons];
    }
}

@end