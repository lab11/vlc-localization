/*
 Copyright (C) 2014 Apple Inc. All Rights Reserved.
 See LICENSE.txt for this sample’s licensing information
 
 Abstract:
 
  Control of camera functions.
  
*/


@import UIKit;

extern NSString * const PFET_URL;
extern NSString * const CAP_URL;
extern NSString * const MEM_URL;
extern NSString * const NINJA_URL;
extern NSString * const PAT_URL;
extern NSString * const TEST_URL;


@interface AAPLCameraViewController : UIViewController <UITableViewDataSource, UITableViewDelegate>

@property (strong, nonatomic) IBOutlet UITableView *tableView;
@property (nonatomic, strong) NSArray *beacons;
@property (strong) NSString *BEACON_UUID;



@end
