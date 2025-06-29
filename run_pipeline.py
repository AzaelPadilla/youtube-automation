import os
import yaml
import logging
from modules.topic_discoverer import discover_topics
from modules.script_generator import generate_script
from modules.tts_engine import synthesize_audio
from modules.video_assembler import assemble_video
from modules.metadata_creator import create_metadata, create_thumbnail
from modules.platform_adapter import upload_short

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def load_configs():
    base = os.path.join(os.path.dirname(__file__), 'configs')
    channel = yaml.safe_load(open(os.path.join(base, 'channel_profile.yaml')))
    fmt = yaml.safe_load(open(os.path.join(base, 'format_profile.yaml')))
    return channel, fmt

def main():
    setup_logging()
    logging.info("Starting YouTube Shorts automation")
    channel_cfg, fmt_cfg = load_configs()

    topic = discover_topics(channel_cfg, fmt_cfg)
    logging.info(f"Topic: {topic}")

    script = generate_script(topic, fmt_cfg)
    logging.info("Script generated")

    audio = synthesize_audio(script, fmt_cfg)
    logging.info(f"Audio: {audio}")

    video = assemble_video(audio, fmt_cfg)
    logging.info(f"Video: {video}")

    meta = create_metadata(topic, fmt_cfg)
    thumb = create_thumbnail(topic, fmt_cfg)
    logging.info(f"Thumbnail: {thumb}")

    upload_short(video, thumb, meta, channel_cfg)
    logging.info("Upload done.")

if __name__ == '__main__':
    main()
