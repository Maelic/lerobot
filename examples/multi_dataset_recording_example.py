#!/usr/bin/env python3
"""
Example script for multi-dataset recording using the new multi_record function.

This example shows how to record data for multiple datasets sequentially within the same episode.
For instance, you can record "pick" and "place" motions as separate datasets but within the same 
continuous episode.

Usage:
```shell
python examples/multi_dataset_recording_example.py
```

Or run the multi_record function directly:
```shell
python -m lerobot.record --config=examples/multi_dataset_recording_example.py
```
"""

from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.record import MultiRecordConfig, MultiDatasetRecordConfig, DatasetRecordConfig
from lerobot.robots.so101_follower import SO101FollowerConfig
from lerobot.teleoperators.so101_leader import SO101LeaderConfig

def create_multi_record_config():
    """Create a configuration for multi-dataset recording."""
    
    # Define the robot configuration
    robot_config = SO101FollowerConfig(
        port="/dev/ttyACM0",  # Adjust to your robot's port
        cameras={
            'up': OpenCVCameraConfig(
                index_or_path=2,
                width=640,
                height=480,
                fps=30
            ),
            'side': OpenCVCameraConfig(
                index_or_path=0,
                width=640,
                height=480,
                fps=30
            )
        },
        id="follower_arm",
    )
    
    # Define teleoperator configuration (optional)
    teleop_config = SO101LeaderConfig(
        port="/dev/ttyACM1",  # Adjust to your teleoperator's port
        id="leader_arm",
    )

    episodes = 2  # Number of episodes should be the same for both datasets
    
    # Define multiple dataset configurations for different stages
    dataset_configs = [
        DatasetRecordConfig(
            repo_id="maelic/pick_knife",
            single_task="Pick up the knife from the table.",
            fps=30,
            episode_time_s=60,  # 30 seconds for pick motion
            reset_time_s=10,
            num_episodes=episodes,
            video=True,
            push_to_hub=False,  # Set to True if you want to upload
            private=True,  # Set to True if you want to keep the dataset private
        ),
        DatasetRecordConfig(
            repo_id="maelic/place_left_knife",
            single_task="Place the knife to the left of the plate.",
            fps=30,
            episode_time_s=60,  # 30 seconds for place motion
            reset_time_s=10,
            num_episodes=episodes,
            video=True,
            push_to_hub=False,  # Set to True if you want to upload
            private=True,  # Set to True if you want to keep the dataset private
        ),
    ]
    
    # Define multi-dataset configuration
    multi_dataset_config = MultiDatasetRecordConfig(
        datasets=dataset_configs,
        stage_switch_keys=["space", "tab"],  # Space for pick, Tab for place
    )
    
    # Create the complete multi-record configuration
    config = MultiRecordConfig(
        robot=robot_config,
        multi_dataset=multi_dataset_config,
        teleop=teleop_config,
        policy=None,  # No policy, using teleop
        display_data=False,
        play_sounds=True,
        resume=False,
    )
    
    return config


def main():
    """Example of how to use multi_record function."""
    from lerobot.record import multi_record
    
    # Create configuration
    config = create_multi_record_config()
    
    print("Starting multi-dataset recording...")
    print("Instructions:")
    print("- Press SPACE to record 'pick' motion to the first dataset")
    print("- Press TAB to record 'place' motion to the second dataset") 
    print("- Press RIGHT ARROW to finish current episode")
    print("- Press LEFT ARROW to re-record current episode")
    print("- Press ESC to stop recording completely")
    print()
    
    # Start multi-dataset recording
    datasets = multi_record(config)
    
    print(f"Recording completed! Created {len(datasets)} datasets:")
    for i, dataset in enumerate(datasets):
        print(f"  Dataset {i}: {dataset.repo_id} with {dataset.num_episodes} episodes")


if __name__ == "__main__":
    main()