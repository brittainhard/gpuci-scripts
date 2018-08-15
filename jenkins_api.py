import jenkinsapi
from jenkinsapi.jenkins import Jenkins


NON_GPU_JOBS = ["goai-docker-container-builder", "gpu-instance-manager"]


def get_jobs():
    jenk = Jenkins("http://18.191.94.64/")
    jobs = []
    for item in jenk.items():
        if str(item[1]) in [str(job) for job in jobs]:
            continue
        elif str(item[1]) in NON_GPU_JOBS:
            continue
        jobs.append(item[1])
    return jobs


def jobs_running(jobs):
    running = [job.is_running() for job in jobs]
    return any(running)


if __name__ == "__main__":
    print(jobs_running(get_jobs()))