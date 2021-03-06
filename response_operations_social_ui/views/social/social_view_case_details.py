from collections import OrderedDict
import logging

from flask import render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import login_required
from structlog import wrap_logger

from response_operations_social_ui.common.social_outcomes import map_social_case_status, map_social_status_groups, \
    get_formatted_social_outcome
from response_operations_social_ui.controllers import case_controller
from response_operations_social_ui.forms import ChangeGroupStatusForm
from response_operations_social_ui.views.social.social_case_context import build_view_social_case_context

logger = wrap_logger(logging.getLogger(__name__))


@login_required
def view_social_case_details(case_id):
    context = build_view_social_case_context(case_id)
    logger.debug("view_social_case_details", case_id=case_id, status=context.get('status'))
    new_iac_tuple = next((category_and_message for category_and_message
                         in get_flashed_messages(with_categories=True)
                         if category_and_message[0] == 'new_iac'), None)
    if new_iac_tuple:
        context['new_iac'] = f'{new_iac_tuple[1][:4]} {new_iac_tuple[1][4:8]} {new_iac_tuple[1][8:]}'

    return render_template('social-view-case-details.html', **context)


@login_required
def change_case_response_status(case_id):
    social_case = case_controller.get_case_by_id(case_id)
    current_status = map_social_case_status(social_case['caseGroup']['caseGroupStatus'])
    sample_unit_reference = social_case['caseGroup']['sampleUnitRef']
    collection_exercise_id = social_case['caseGroup']['collectionExerciseId']

    statuses = case_controller.get_available_case_group_statuses_direct(collection_exercise_id, sample_unit_reference)
    available_events = filter_and_format_available_events(statuses)

    grouped_events = group_and_order_events(available_events, statuses)

    return render_template('social-change-response-status.html', current_status=current_status,
                           reference=sample_unit_reference, statuses=grouped_events)


def filter_and_format_available_events(statuses: dict) -> dict:
    available_events = {event: get_formatted_social_outcome(event)
                        for event, status in statuses.items()
                        if case_controller.is_allowed_change_social_status(status)}
    return available_events


def group_and_order_events(available_events: dict, statuses: dict) -> OrderedDict:
    grouped_events = OrderedDict()
    for event, formatted_event in sorted(available_events.items(), key=lambda pair: pair[1]):
        if not grouped_events.get(map_social_status_groups(statuses[event])):
            grouped_events[map_social_status_groups(statuses[event])] = OrderedDict()
        grouped_events[map_social_status_groups(statuses[event])][event] = formatted_event
    return grouped_events


@login_required
def update_case_response_status(case_id):
    form = ChangeGroupStatusForm(request.form)
    case_controller.post_case_event(case_id=case_id,
                                    category=form.event.data,
                                    description="Transitioning case group status")
    flash('Status changed successfully', 'success')
    return redirect(url_for('social_bp.view_social_case_details', case_id=case_id,
                            status_updated=True,
                            updated_status=form.event.data))
