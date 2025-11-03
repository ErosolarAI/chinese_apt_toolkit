# Energy Company Campaign

This campaign is designed to target energy companies, with the goal of disrupting the power grid.

## Objectives

- Infiltrate target networks
- Disrupt the power grid
- Establish long-term persistence

## Tools

This campaign will use a variety of custom and off-the-shelf tools to achieve its objectives. These tools will be stored in the `tools` directory.

## Payloads

The payloads for this campaign will be stored in the `payloads` directory. These payloads will be designed to be highly evasive and difficult to detect.

## Running a Real Campaign

This campaign can be configured to run against real targets for authorized penetration testing.

To run a real campaign, you will need to create a `config.json` file in this directory. You can use the `config.json.example` file as a template.

Populate the `config.json` file with the actual information for your authorized target.

Once you have configured your target, you can run the campaign using the following command:

```
python run_campaign.py
```
